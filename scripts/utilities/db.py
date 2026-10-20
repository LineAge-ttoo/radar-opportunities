import sqlite3
import json
import os
from datetime import datetime, timezone

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, 'data', 'opportunities', 'radar.db')
DEFAULT_JSONL_PATH = os.path.join(BASE_DIR, 'data', 'opportunities', 'opportunities.jsonl')
DEFAULT_LATEST_JSON = os.path.join(BASE_DIR, 'data', 'opportunities', 'latest_scan.json')

def get_connection(db_path=DEFAULT_DB_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=DEFAULT_DB_PATH):
    conn = get_connection(db_path)
    cur = conn.cursor()
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS opportunities (
        opportunity_id TEXT PRIMARY KEY,
        source TEXT NOT NULL,
        source_url TEXT NOT NULL,
        discovered_at TEXT NOT NULL,
        published_at TEXT,
        title TEXT NOT NULL,
        organization TEXT,
        description TEXT,
        category TEXT,
        opportunity_type TEXT,
        payment_min REAL,
        payment_max REAL,
        currency TEXT,
        location TEXT,
        remote INTEGER DEFAULT 1,
        skills_json TEXT,
        raw_data_json TEXT,
        observed_data_json TEXT,
        estimated_data_json TEXT,
        proposal_json TEXT,
        blueprint_json TEXT,
        fit_score REAL,
        money_score REAL,
        difficulty_score REAL,
        trust_score REAL,
        reusability_score REAL,
        scalability_score REAL,
        competition_score REAL,
        overall_score REAL,
        decision TEXT,
        reasoning TEXT,
        next_action TEXT,
        first_seen_at TEXT,
        last_seen_at TEXT,
        contacted_at TEXT,
        notes TEXT,
        status TEXT DEFAULT 'NUEVA'
    )
    ''')

    columns_to_check = [
        ('proposal_json', 'TEXT'),
        ('blueprint_json', 'TEXT'),
        ('contacted_at', 'TEXT'),
        ('notes', 'TEXT')
    ]
    cur.execute("PRAGMA table_info(opportunities);")
    existing_cols = [row['name'] for row in cur.fetchall()]
    for col_name, col_type in columns_to_check:
        if col_name not in existing_cols:
            try:
                cur.execute(f"ALTER TABLE opportunities ADD COLUMN {col_name} {col_type};")
            except Exception:
                pass

    cur.execute('CREATE INDEX IF NOT EXISTS idx_opp_decision ON opportunities(decision);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_opp_score ON opportunities(overall_score DESC);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_opp_source ON opportunities(source);')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_opp_status ON opportunities(status);')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS scans (
        scan_id TEXT PRIMARY KEY,
        started_at TEXT NOT NULL,
        finished_at TEXT,
        sources_consulted TEXT,
        total_found INTEGER DEFAULT 0,
        prioridad_count INTEGER DEFAULT 0,
        investigar_count INTEGER DEFAULT 0,
        observar_count INTEGER DEFAULT 0,
        descartar_count INTEGER DEFAULT 0,
        construir_vender_count INTEGER DEFAULT 0,
        execution_notes TEXT
    )
    ''')

    conn.commit()
    conn.close()

def save_opportunities(opportunities, scan_id=None, db_path=DEFAULT_DB_PATH, jsonl_path=DEFAULT_JSONL_PATH):
    init_db(db_path)
    conn = get_connection(db_path)
    cur = conn.cursor()
    now_iso = datetime.now(timezone.utc).isoformat()

    saved_count = 0
    updated_count = 0

    os.makedirs(os.path.dirname(jsonl_path), exist_ok=True)
    with open(jsonl_path, 'a', encoding='utf-8') as jf:
        for opp in opportunities:
            opp_id = opp['opportunity_id']
            jf.write(json.dumps(opp, ensure_ascii=False) + '\n')

            cur.execute('SELECT opportunity_id, first_seen_at, status FROM opportunities WHERE opportunity_id = ?', (opp_id,))
            row = cur.fetchone()

            first_seen = row['first_seen_at'] if row else now_iso
            current_status = row['status'] if (row and row['status'] not in ['NEW', None, '']) else 'NUEVA'
            last_seen = now_iso

            cur.execute('''
            INSERT INTO opportunities (
                opportunity_id, source, source_url, discovered_at, published_at,
                title, organization, description, category, opportunity_type,
                payment_min, payment_max, currency, location, remote,
                skills_json, raw_data_json, observed_data_json, estimated_data_json,
                proposal_json, blueprint_json,
                fit_score, money_score, difficulty_score, trust_score,
                reusability_score, scalability_score, competition_score, overall_score,
                decision, reasoning, next_action, first_seen_at, last_seen_at, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(opportunity_id) DO UPDATE SET
                source_url = excluded.source_url,
                title = excluded.title,
                organization = excluded.organization,
                description = excluded.description,
                published_at = excluded.published_at,
                payment_min = excluded.payment_min,
                payment_max = excluded.payment_max,
                currency = excluded.currency,
                skills_json = excluded.skills_json,
                raw_data_json = excluded.raw_data_json,
                observed_data_json = excluded.observed_data_json,
                estimated_data_json = excluded.estimated_data_json,
                proposal_json = excluded.proposal_json,
                blueprint_json = excluded.blueprint_json,
                fit_score = excluded.fit_score,
                money_score = excluded.money_score,
                difficulty_score = excluded.difficulty_score,
                trust_score = excluded.trust_score,
                reusability_score = excluded.reusability_score,
                scalability_score = excluded.scalability_score,
                competition_score = excluded.competition_score,
                overall_score = excluded.overall_score,
                decision = excluded.decision,
                reasoning = excluded.reasoning,
                next_action = excluded.next_action,
                last_seen_at = excluded.last_seen_at,
                status = CASE WHEN opportunities.status = 'NEW' THEN 'NUEVA' ELSE opportunities.status END
            ''', (
                opp_id,
                opp.get('source', 'Unknown'),
                opp.get('source_url', ''),
                opp.get('discovered_at', now_iso),
                opp.get('published_at'),
                opp.get('title', ''),
                opp.get('organization', ''),
                opp.get('description', ''),
                opp.get('category', ''),
                opp.get('opportunity_type', 'general'),
                opp.get('payment_min'),
                opp.get('payment_max'),
                opp.get('currency'),
                opp.get('location', ''),
                1 if opp.get('remote', True) else 0,
                json.dumps(opp.get('skills', []), ensure_ascii=False),
                json.dumps(opp.get('raw_data', {}), ensure_ascii=False),
                json.dumps(opp.get('observed_data', {}), ensure_ascii=False),
                json.dumps(opp.get('estimated_data', {}), ensure_ascii=False),
                json.dumps(opp.get('proposal', {}), ensure_ascii=False) if opp.get('proposal') else None,
                json.dumps(opp.get('blueprint', {}), ensure_ascii=False) if opp.get('blueprint') else None,
                opp.get('fit_score', 0.0),
                opp.get('money_score', 0.0),
                opp.get('difficulty_score', 0.0),
                opp.get('trust_score', 0.0),
                opp.get('reusability_score', 0.0),
                opp.get('scalability_score', 0.0),
                opp.get('competition_score', 0.0),
                opp.get('overall_score', 0.0),
                opp.get('decision', 'OBSERVAR'),
                opp.get('reasoning', ''),
                opp.get('next_action', ''),
                first_seen,
                last_seen,
                current_status
            ))
            if row:
                updated_count += 1
            else:
                saved_count += 1

    conn.commit()
    conn.close()
    return saved_count, updated_count

def update_opportunity_status(opp_id, new_status, notes=None, db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    conn = get_connection(db_path)
    cur = conn.cursor()
    now_iso = datetime.now(timezone.utc).isoformat()

    if new_status in ['PROPUESTA_ENVIADA', 'EN_NEGOCIACION']:
        cur.execute('''
        UPDATE opportunities 
        SET status = ?, notes = COALESCE(?, notes), contacted_at = COALESCE(contacted_at, ?)
        WHERE opportunity_id = ?
        ''', (new_status, notes, now_iso, opp_id))
    else:
        cur.execute('''
        UPDATE opportunities 
        SET status = ?, notes = COALESCE(?, notes)
        WHERE opportunity_id = ?
        ''', (new_status, notes, opp_id))
    
    conn.commit()
    conn.close()

def log_scan_run(scan_data, db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute('''
    INSERT OR REPLACE INTO scans (
        scan_id, started_at, finished_at, sources_consulted, total_found,
        prioridad_count, investigar_count, observar_count, descartar_count,
        construir_vender_count, execution_notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        scan_data['scan_id'],
        scan_data['started_at'],
        scan_data.get('finished_at', datetime.now(timezone.utc).isoformat()),
        json.dumps(scan_data.get('sources_consulted', []), ensure_ascii=False),
        scan_data.get('total_found', 0),
        scan_data.get('prioridad_count', 0),
        scan_data.get('investigar_count', 0),
        scan_data.get('observar_count', 0),
        scan_data.get('descartar_count', 0),
        scan_data.get('construir_vender_count', 0),
        scan_data.get('execution_notes', '')
    ))
    conn.commit()
    conn.close()

def get_all_opportunities(filter_decision=None, filter_status=None, limit=250, db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    conn = get_connection(db_path)
    cur = conn.cursor()

    query = 'SELECT * FROM opportunities'
    params = []
    conditions = ["decision != 'DESCARTAR'"]

    if filter_decision:
        conditions = ['decision = ?']
        params.append(filter_decision)
    if filter_status:
        conditions.append('status = ?')
        params.append(filter_status)

    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    query += ' ORDER BY overall_score DESC, published_at DESC LIMIT ?'
    params.append(limit)

    cur.execute(query, params)
    rows = cur.fetchall()
    
    results = []
    for r in rows:
        d = dict(r)
        d['skills'] = json.loads(d.get('skills_json') or '[]')
        d['raw_data'] = json.loads(d.get('raw_data_json') or '{}')
        d['observed_data'] = json.loads(d.get('observed_data_json') or '{}')
        d['estimated_data'] = json.loads(d.get('estimated_data_json') or '{}')
        d['proposal'] = json.loads(d.get('proposal_json') or '{}') if d.get('proposal_json') else None
        d['blueprint'] = json.loads(d.get('blueprint_json') or '{}') if d.get('blueprint_json') else None
        raw = d['raw_data']
        obs = d['observed_data']
        d['contact_phone'] = raw.get('contact_phone') or obs.get('contact_phone') or obs.get('whatsapp_phone') or raw.get('whatsapp_phone') or ''
        d['contact_whatsapp_url'] = raw.get('contact_whatsapp_url') or obs.get('contact_whatsapp_url') or ''
        d['circular_code'] = raw.get('circular_code') or obs.get('circular_code') or ''
        d['contact_email'] = raw.get('contact_email') or obs.get('contact_email') or ''
        results.append(d)

    conn.close()
    return results

def get_stats(db_path=DEFAULT_DB_PATH):
    init_db(db_path)
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute('SELECT COUNT(*) FROM opportunities;')
    total = cur.fetchone()[0]

    cur.execute('SELECT decision, COUNT(*) FROM opportunities GROUP BY decision;')
    by_decision = dict(cur.fetchall())

    cur.execute('SELECT status, COUNT(*) FROM opportunities GROUP BY status;')
    by_status = dict(cur.fetchall())

    conn.close()
    return {
        'total': total,
        'by_decision': by_decision,
        'by_status': by_status
    }
