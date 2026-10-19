import sys
import os
import json
import uuid
from datetime import datetime, timezone

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from scripts.collectors.collector_manager import CollectorManager
from scripts.analyzers.normalizer import OpportunityNormalizer
from scripts.analyzers.scoring_engine import ScoringEngine
from scripts.analyzers.proposal_generator import TechnicalProposalGenerator
from scripts.analyzers.blueprint_generator import BlueprintGenerator
from scripts.utilities.db import save_opportunities, log_scan_run, get_all_opportunities, get_stats
from scripts.utilities.presenter import RadarPresenter

def run_scan():
    scan_id = f"scan_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:6]}"
    started_at = datetime.now(timezone.utc).isoformat()

    print(f"=== RADAR SCAN INICIADO [{scan_id}] ===")
    print(f"Hora de inicio: {started_at}")

    # 1. Collect
    mgr = CollectorManager()
    raw_results = mgr.run_all()

    # 2. Normalize
    normalized_list = []
    sources_consulted = []

    for source_name, result in raw_results.items():
        sources_consulted.append(source_name)
        if not result['success']:
            print(f"Advertencia: Fuente '{source_name}' reporto: {result.get('error')}")
            continue

        items = result['items']
        print(f"Fuente '{source_name}': {len(items)} items recibidos.")

        for item in items:
            if source_name == 'Remotive':
                norm = OpportunityNormalizer.normalize_remotive(item)
            elif source_name == 'Arbeitnow':
                norm = OpportunityNormalizer.normalize_arbeitnow(item)
            elif source_name == 'RemoteOK':
                norm = OpportunityNormalizer.normalize_remoteok(item)
            elif source_name == 'WeWorkRemotely':
                norm = OpportunityNormalizer.normalize_weworkremotely(item)
            elif source_name == 'HackerNews':
                norm = OpportunityNormalizer.normalize_hackernews(item)
            elif source_name == 'GitHub Bounties':
                norm = OpportunityNormalizer.normalize_github_bounty(item)
            else:
                continue
            normalized_list.append(norm)

    print(f"Total oportunidades recolectadas y normalizadas: {len(normalized_list)}")

    # 3. Score & Classify + Generate Proposals / Blueprints
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
        dec = scored.get('decision', 'OBSERVAR')
        counts[dec] = counts.get(dec, 0) + 1

        if dec in ['PRIORIDAD', 'INVESTIGAR', 'CONSTRUIR_Y_VENDER', 'OBSERVAR']:
            scored['proposal'] = TechnicalProposalGenerator.generate_pitch(scored)
        else:
            scored['proposal'] = None

        if dec in ['CONSTRUIR_Y_VENDER', 'PRIORIDAD']:
            scored['blueprint'] = BlueprintGenerator.generate_blueprint(scored)
        else:
            scored['blueprint'] = None

        scored_list.append(scored)

    # 4. Sort by overall_score DESC, then freshness
    scored_list.sort(
        key=lambda x: (
            x.get('overall_score', 0),
            -float(x.get('estimated_data', {}).get('age_hours', 9999))
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
        'execution_notes': f"Scan multi-fuente ({', '.join(sources_consulted)}) con motor v2 (Freshness + Sniper Pitch + Blueprint)."
    }

    # 5. Persist to DB, JSONL, latest JSON
    saved_count, updated_count = save_opportunities(scored_list, scan_id=scan_id)
    log_scan_run(scan_meta)

    # Filter actionable opportunities for web export (exclude DESCARTAR noise)
    actionable_opps = [o for o in scored_list if o.get('decision') != 'DESCARTAR']
    db_stats = get_stats()

    payload_out = {
        'meta': scan_meta,
        'stats': db_stats,
        'opportunities': actionable_opps[:250]
    }

    # Save latest scan JSON in data/opportunities, app/, and root for static web hosting (Vercel / GitHub Pages)
    for rel_target in [
        os.path.join('data', 'opportunities', 'latest_scan.json'),
        os.path.join('app', 'latest_scan.json'),
        'latest_scan.json'
    ]:
        target_p = os.path.join(BASE_DIR, rel_target)
        os.makedirs(os.path.dirname(target_p) or BASE_DIR, exist_ok=True)
        with open(target_p, 'w', encoding='utf-8') as f:
            json.dump(payload_out, f, ensure_ascii=False, indent=2)

    # Save summary JSON
    summary_path = os.path.join(BASE_DIR, 'exports', 'RADAR_SUMMARY.json')
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(scan_meta, f, ensure_ascii=False, indent=2)

    # 6. Generate Markdown and HTML presentations
    presenter = RadarPresenter(export_dir=os.path.join(BASE_DIR, 'exports'))
    md_file = presenter.generate_markdown(scan_meta, actionable_opps)
    html_file = presenter.generate_html(scan_meta, actionable_opps)

    print("\n" + "="*52)
    print(" RADAR SCAN SUMMARY v2 (FRESHNESS & REVENUE ENGINE)")
    print("="*52)
    print(f"Fecha / Hora:           {started_at}")
    print(f"Fuentes Consultadas:    {', '.join(sources_consulted)}")
    print(f"Hallazgos Totales:      {len(scored_list)} (Accionables: {len(actionable_opps)})")
    print(f"  - CONSTRUIR Y VENDER:  {counts.get('CONSTRUIR_Y_VENDER', 0)}")
    print(f"  - PRIORIDAD:           {counts.get('PRIORIDAD', 0)}")
    print(f"  - INVESTIGAR:          {counts.get('INVESTIGAR', 0)}")
    print(f"  - OBSERVAR:            {counts.get('OBSERVAR', 0)}")
    print(f"  - DESCARTAR:           {counts.get('DESCARTAR', 0)}")
    print(f"Nuevas guardadas:       {saved_count} (Actualizadas: {updated_count})")
    print("="*52 + "\n")

    return scan_meta, actionable_opps

if __name__ == '__main__':
    run_scan()
