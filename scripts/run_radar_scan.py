import sys
import os
import json
import uuid
import sqlite3
from datetime import datetime, timezone

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from scripts.collectors.collector_manager import CollectorManager
from scripts.analyzers.normalizer import OpportunityNormalizer
from scripts.analyzers.scoring_engine import ScoringEngine
from scripts.analyzers.proposal_generator import TechnicalProposalGenerator
from scripts.analyzers.blueprint_generator import BlueprintGenerator
from scripts.utilities.db import save_opportunities, log_scan_run, get_all_opportunities, get_stats, DEFAULT_DB_PATH
from scripts.utilities.presenter import RadarPresenter

def purge_corporate_engineering_noise():
    """Removes old corporate engineering jobs so only doable Colombia/practical tasks exist."""
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

def run_scan():
    scan_id = f"scan_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:6]}"
    started_at = datetime.now(timezone.utc).isoformat()

    print(f"=== RADAR COLOMBIA & TAREAS PRACTICAS [{scan_id}] ===")
    purge_corporate_engineering_noise()

    mgr = CollectorManager()
    raw_results = mgr.run_all()

    normalized_list = []
    sources_consulted = []

    for source_name, result in raw_results.items():
        sources_consulted.append(source_name)
        if not result['success']:
            print(f"Advertencia: Fuente '{source_name}' reporto: {result.get('error')}")
            continue

        items = result['items']
        print(f"Fuente '{source_name}': {len(items)} oportunidades recibidas.")

        for item in items:
            if 'Clientes Colombia' in source_name:
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

    # Sort: Colombia first, then highest score, then newest
    scored_list.sort(
        key=lambda x: (
            1 if x.get('estimated_data', {}).get('is_colombia') else 0,
            x.get('overall_score', 0),
            -float(x.get('estimated_data', {}).get('age_hours', 999))
        ),
        reverse=True
    )

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
        'execution_notes': 'Escaneo orientado a Clientes en Colombia (Instagram, Facebook, Workana CO) y tareas prácticas (Automatizaciones, Planos, 3D, Web) sin contratos legales.'
    }

    save_opportunities(scored_list, scan_id=scan_id)
    purge_corporate_engineering_noise()
    log_scan_run(scan_meta)

    db_stats = get_stats()
    payload_out = {
        'meta': scan_meta,
        'stats': db_stats,
        'opportunities': scored_list[:200]
    }

    for rel_target in [
        os.path.join('data', 'opportunities', 'latest_scan.json'),
        os.path.join('app', 'latest_scan.json'),
        'latest_scan.json'
    ]:
        target_p = os.path.join(BASE_DIR, rel_target)
        os.makedirs(os.path.dirname(target_p) or BASE_DIR, exist_ok=True)
        with open(target_p, 'w', encoding='utf-8') as f:
            json.dump(payload_out, f, ensure_ascii=False, indent=2)

    summary_path = os.path.join(BASE_DIR, 'exports', 'RADAR_SUMMARY.json')
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(scan_meta, f, ensure_ascii=False, indent=2)

    presenter = RadarPresenter(export_dir=os.path.join(BASE_DIR, 'exports'))
    presenter.generate_markdown(scan_meta, scored_list)
    presenter.generate_html(scan_meta, scored_list)

    print("\n" + "="*56)
    print(" RADAR COLOMBIA — RESUMEN DE TRABAJOS QUE SÍ PUEDES HACER")
    print("="*56)
    print(f"Fuentes Consultadas:    {', '.join(sources_consulted)}")
    print(f"Trabajos Viables Hoy:   {len(scored_list)} (Descartados por ser de ingeniería/otros: {counts.get('DESCARTAR', 0)})")
    print(f"  - PRIORIDAD:           {counts.get('PRIORIDAD', 0)}")
    print(f"  - CONSTRUIR Y VENDER:  {counts.get('CONSTRUIR_Y_VENDER', 0)}")
    print(f"  - INVESTIGAR:          {counts.get('INVESTIGAR', 0)}")
    print("="*56 + "\n")

    return scan_meta, scored_list

if __name__ == '__main__':
    run_scan()
