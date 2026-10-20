import sys
import os
import json
import uuid
import sqlite3
import urllib.parse
from datetime import datetime, timezone

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from scripts.collectors.collector_manager import CollectorManager
from scripts.analyzers.normalizer import OpportunityNormalizer
from scripts.analyzers.scoring_engine import ScoringEngine
from scripts.analyzers.proposal_generator import TechnicalProposalGenerator
from scripts.analyzers.blueprint_generator import BlueprintGenerator
from scripts.utilities.db import save_opportunities, log_scan_run, get_stats, DEFAULT_DB_PATH
from scripts.utilities.presenter import RadarPresenter
from scripts.utilities.whatsapp_auto_sender import auto_dispatch_to_whatsapp_3222739034

USER_WHATSAPP_CO = "573222739034"


def purge_old_and_invalid_links():
    """Elimina cualquier registro antiguo sin enlace real o que apunte a búsquedas genéricas de Maps o logins de SECOP."""
    try:
        conn = sqlite3.connect(DEFAULT_DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM opportunities
            WHERE opportunity_id LIKE 'remotive_%'
               OR opportunity_id LIKE 'arbeitnow_%'
               OR opportunity_id LIKE 'remoteok_%'
               OR opportunity_id LIKE 'wwr_%'
               OR opportunity_id LIKE 'hn_%'
               OR opportunity_id LIKE 'github_%'
               OR opportunity_id IN ('huila_guadua_01','huila_guadua_02','huila_alcaldia_01','huila_alcaldia_02','estudiantes_01','estudiantes_02','blender_guadua_03')
               OR source_url LIKE '%google.com/maps/search%'
               OR source_url LIKE '%google.com/search%'
               OR source_url LIKE '%STS/Users/Login%'
               OR decision = 'DESCARTAR';
        """)
        conn.commit()
        conn.close()
    except Exception:
        pass


def run_scan():
    scan_id = f"scan_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:6]}"
    started_at = datetime.now(timezone.utc).isoformat()

    print(f"=== QUE HAY PA HACER! · SAN AGUSTIN HUILA & COLOMBIA [{scan_id}] ===")
    purge_old_and_invalid_links()

    mgr = CollectorManager()
    raw_results = mgr.run_all()

    normalized_list = []
    sources_consulted = []

    for source_name, result in raw_results.items():
        sources_consulted.append(source_name)
        if not result.get('success'):
            print(f"Advertencia: Fuente '{source_name}' reporto: {result.get('error')}")
            continue

        items = result.get('items', [])
        print(f"Fuente '{source_name}': {len(items)} oportunidades recibidas.")

        for item in items:
            if 'San Agustín' in source_name or 'Huila' in source_name:
                norm = OpportunityNormalizer.normalize_san_agustin_huila(item)
            elif 'Clientes Colombia' in source_name:
                norm = OpportunityNormalizer.normalize_colombia_social(item)
            elif 'Workana' in source_name:
                norm = OpportunityNormalizer.normalize_workana(item)
            elif 'Freelancer' in source_name:
                norm = OpportunityNormalizer.normalize_freelancer(item)
            else:
                continue
            normalized_list.append(norm)

    scoring_engine = ScoringEngine()
    scored_list = []
    counts = {
        'PRIORIDAD': 0,
        'CONSTRUIR_Y_VENDER': 0,
        'INVESTIGAR': 0,
        'OBSERVAR': 0,
        'DESCARTAR': 0
    }

    for opp in normalized_list:
        # Bloquear cualquier URL que no sea contacto directo o circular real
        s_url = str(opp.get('source_url') or '')
        if 'google.com/maps/search' in s_url or 'STS/Users/Login' in s_url:
            continue

        scored = scoring_engine.analyze(opp)
        dec = scored.get('decision', 'DESCARTAR')
        counts[dec] = counts.get(dec, 0) + 1

        if dec == 'DESCARTAR':
            continue

        scored['proposal'] = TechnicalProposalGenerator.generate_pitch(scored)
        scored['blueprint'] = BlueprintGenerator.generate_blueprint(scored)
        scored_list.append(scored)

    # Priorizar: 1. Con WhatsApp Directo en San Agustín / Huila, 2. Circulares Reales SECOP Huila, 3. Más recientes primero
    scored_list.sort(
        key=lambda x: (
            1 if (x.get('estimated_data', {}).get('is_huila_guadua') and x.get('observed_data', {}).get('whatsapp_phone')) else 0,
            1 if x.get('estimated_data', {}).get('is_huila_guadua') else 0,
            1 if x.get('observed_data', {}).get('whatsapp_phone') else 0,
            -float(x.get('estimated_data', {}).get('age_hours', 999)),
            x.get('overall_score', 0)
        ),
        reverse=True
    )

    # Envío automático a +57 3222739034 sin intervención manual
    wa_auto_result = auto_dispatch_to_whatsapp_3222739034(scored_list)

    finished_at = datetime.now(timezone.utc).isoformat()
    scan_meta = {
        'scan_id': scan_id,
        'started_at': started_at,
        'finished_at': finished_at,
        'sources_consulted': sources_consulted,
        'total_found': len(scored_list),
        'prioridad_count': counts.get('PRIORIDAD', 0),
        'construir_vender_count': counts.get('CONSTRUIR_Y_VENDER', 0),
        'investigar_count': counts.get('INVESTIGAR', 0),
        'observar_count': counts.get('OBSERVAR', 0),
        'descartar_count': counts.get('DESCARTAR', 0),
        'whatsapp_target': USER_WHATSAPP_CO,
        'whatsapp_auto_dispatched': wa_auto_result.get('dispatched', False),
        'execution_notes': 'Contactos reales verificados (WhatsApp directo +57 de solicitantes en San Agustín/Pitalito/Isnos, Circulares Reales SECOP II sin clave y Proyectos Activos Workana/Freelancer) + Auto-envío a WhatsApp 3222739034.'
    }

    save_opportunities(scored_list, scan_id=scan_id)
    purge_old_and_invalid_links()
    log_scan_run(scan_meta)

    db_stats = get_stats()
    payload_out = {
        'meta': scan_meta,
        'stats': db_stats,
        'whatsapp_alert': wa_auto_result,
        'opportunities': scored_list[:200]
    }

    for rel_target in [
        os.path.join('data', 'opportunities', 'latest_scan.json'),
        os.path.join('data', 'opportunities', 'whatsapp_alert_3222739034.json'),
        os.path.join('app', 'latest_scan.json'),
        'latest_scan.json'
    ]:
        target_p = os.path.join(BASE_DIR, rel_target)
        os.makedirs(os.path.dirname(target_p) or BASE_DIR, exist_ok=True)
        with open(target_p, 'w', encoding='utf-8') as f:
            json.dump(wa_auto_result if 'whatsapp_alert_' in rel_target else payload_out, f, ensure_ascii=False, indent=2)

    summary_path = os.path.join(BASE_DIR, 'exports', 'RADAR_SUMMARY.json')
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(scan_meta, f, ensure_ascii=False, indent=2)

    presenter = RadarPresenter(export_dir=os.path.join(BASE_DIR, 'exports'))
    presenter.generate_markdown(scan_meta, scored_list)
    presenter.generate_html(scan_meta, scored_list)

    print("\n" + "="*62)
    print(" QUE HAY PA´ HACER! — CONTACTOS REALES & AUTO-WHATSAPP")
    print("="*62)
    print(f"Fuentes Consultadas:    {', '.join(sources_consulted)}")
    print(f"Trabajos Con Contacto:  {len(scored_list)}")
    print(f"Auto-Envío WhatsApp:    +57 322 273 9034 -> {wa_auto_result.get('methods')}")
    print("="*62 + "\n")

    return scan_meta, scored_list


if __name__ == '__main__':
    run_scan()
