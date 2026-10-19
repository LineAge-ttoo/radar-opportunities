import sys
import os
import json
import uuid
import sqlite3
import urllib.parse
import requests
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

USER_WHATSAPP_CO = "573222739034"


def purge_corporate_engineering_noise():
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
               OR decision = 'DESCARTAR';
        """)
        conn.commit()
        conn.close()
    except Exception:
        pass


def build_whatsapp_digest_for_3222739034(scored_list):
    """
    Construye el mensaje ejecutivo de oportunidades de alto potencial
    para enviar al WhatsApp del usuario en San Agustín Huila: +57 3222739034.
    """
    top_items = [
        o for o in scored_list
        if o.get('overall_score', 0) >= 88 or o.get('estimated_data', {}).get('is_huila_guadua')
    ][:8]

    lines = [
        "🔔 *QUE HAY PA´ HACER! — ALERTA DE ALTO POTENCIAL*",
        "📍 *Zona:* San Agustín, Huila & Colombia",
        f"🕒 *Actualizado:* {datetime.now().strftime('%Y-%m-%d %I:%M %p')}",
        ""
    ]
    for idx, o in enumerate(top_items, 1):
        sal = o.get('observed_data', {}).get('stated_salary') or 'Por cotizar'
        lines.append(
            f"*{idx}. {o.get('title', '')[:75]}*\n"
            f"   💰 {sal} | 📌 {o.get('source', '')}\n"
            f"   🔗 {o.get('source_url', '')}"
        )

    msg_text = "\n".join(lines)
    wa_url = f"https://wa.me/{USER_WHATSAPP_CO}?text={urllib.parse.quote(msg_text)}"

    # Si el usuario configura CallMeBot API Key o Webhook en variables de entorno, envía push silencioso automático
    callmebot_key = os.environ.get("RADAR_CALLMEBOT_APIKEY")
    if callmebot_key:
        try:
            requests.get(
                f"https://api.callmebot.com/whatsapp.php?phone={USER_WHATSAPP_CO}&text={urllib.parse.quote(msg_text)}&apikey={callmebot_key}",
                timeout=8
            )
        except Exception:
            pass

    return {
        "target_phone": USER_WHATSAPP_CO,
        "display_phone": "+57 322 273 9034",
        "high_potential_count": len(top_items),
        "message_text": msg_text,
        "wa_me_url": wa_url,
        "generated_at": datetime.now(timezone.utc).isoformat()
    }


def run_scan():
    scan_id = f"scan_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:6]}"
    started_at = datetime.now(timezone.utc).isoformat()

    print(f"=== QUE HAY PA HACER! · SAN AGUSTIN HUILA & COLOMBIA [{scan_id}] ===")
    purge_corporate_engineering_noise()

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
        scored = scoring_engine.analyze(opp)
        dec = scored.get('decision', 'DESCARTAR')
        counts[dec] = counts.get(dec, 0) + 1

        if dec == 'DESCARTAR':
            continue

        scored['proposal'] = TechnicalProposalGenerator.generate_pitch(scored)
        scored['blueprint'] = BlueprintGenerator.generate_blueprint(scored)
        scored_list.append(scored)

    # Priorizar: 1. San Agustín Huila / Guadua / Estudiantes, 2. Más recientes primero, 3. Colombia, 4. Mayor puntaje
    scored_list.sort(
        key=lambda x: (
            1 if x.get('estimated_data', {}).get('is_huila_guadua') else 0,
            1 if x.get('estimated_data', {}).get('is_colombia') else 0,
            -float(x.get('estimated_data', {}).get('age_hours', 999)),
            x.get('overall_score', 0)
        ),
        reverse=True
    )

    wa_alert = build_whatsapp_digest_for_3222739034(scored_list)

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
        'execution_notes': 'Escaneo diario multi-horario enfocado en San Agustín Huila, Cabañas en Guadua, Alcaldías (SECOP II), Estudiantes/Universitarios, Blender 3D y Clientes en Colombia.'
    }

    save_opportunities(scored_list, scan_id=scan_id)
    purge_corporate_engineering_noise()
    log_scan_run(scan_meta)

    db_stats = get_stats()
    payload_out = {
        'meta': scan_meta,
        'stats': db_stats,
        'whatsapp_alert': wa_alert,
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
            json.dump(wa_alert if 'whatsapp_alert_' in rel_target else payload_out, f, ensure_ascii=False, indent=2)

    summary_path = os.path.join(BASE_DIR, 'exports', 'RADAR_SUMMARY.json')
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(scan_meta, f, ensure_ascii=False, indent=2)

    presenter = RadarPresenter(export_dir=os.path.join(BASE_DIR, 'exports'))
    presenter.generate_markdown(scan_meta, scored_list)
    presenter.generate_html(scan_meta, scored_list)

    print("\n" + "="*62)
    print(" QUE HAY PA´ HACER! — SAN AGUSTÍN HUILA · GUADUA · ESTUDIANTES")
    print("="*62)
    print(f"Fuentes Consultadas:    {', '.join(sources_consulted)}")
    print(f"Trabajos Viables Hoy:   {len(scored_list)}")
    print(f"WhatsApp Notificación:  +57 322 273 9034 ({wa_alert['high_potential_count']} de alto potencial)")
    print("="*62 + "\n")

    return scan_meta, scored_list


if __name__ == '__main__':
    run_scan()
