import sqlite3
import json
import os
from datetime import datetime

DEFAULT_DB_PATH = r'C:\Radar\data\opportunities\radar.db'
DEFAULT_JSONL_PATH = r'C:\Radar\data\opportunities\opportunities.jsonl'
DEFAULT_LATEST_JSON = r'C:\Radar\data\opportunities\latest_scan.json'

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
        status TEXT DEFAULT 'NEW'
    )
    ''')

    cur.execute('''
    CREATE INDEX IF NOT EXISTS idx_opp_decision ON opportunities(decision);
    ''')
    cur.execute('''
    CREATE INDEX IF NOT EXISTS idx_opp_score ON opportunities(overall_score DESC);
    ''')
    cur.execute('''
    CREATE INDEX IF NOT EXISTS idx_opp_source ON opportunities(source);
    ''')

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
    now_iso = datetime.now().isoformat()

    saved_count = 0
    updated_count = 0

    os.makedirs(os.path.dirname(jsonl_path), exist_ok=True)
    with open(jsonl_path, 'a', encoding='utf-8') as jf:
        for opp in opportunities:
            opp_id = opp['opportunity_id']
            jf.write(json.dumps(opp, ensure_ascii=False) + '\n')

            cur.execute('SELECT opportunity_id, first_seen_at FROM opportunities WHERE opportunity_id = ?', (opp_id,))
            row = cur.fetchone()

            first_seen = row['first_seen_at'] if row else now_iso
            last_seen = now_iso

            cur.execute('''
            INSERT INTO opportunities (
                opportunity_id, source, source_url, discovered_at, published_at,
                title, organization, description, category, opportunity_type,
                payment_min, payment_max, currency, location, remote,
                skills_json, raw_data_json, observed_data_json, estimated_data_json,
                fit_score, money_score, difficulty_score, trust_score,
                reusability_score, scalability_score, competition_score, overall_score,
                decision, reasoning, next_action, first_seen_at, last_seen_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(opportunity_id) DO UPDATE SET
                title = excluded.title,
                organization = excluded.organization,
                description = excluded.description,
                payment_min = excluded.payment_min,
                payment_max = excluded.payment_max,
                currency = excluded.currency,
                skills_json = excluded.skills_json,
                observed_data_json = excluded.observed_data_json,
                estimated_data_json = excluded.estimated_data_json,
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
                last_seen_at = excluded.last_seen_at
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
                last_seen
            ))
            if row:
                updated_count += 1
            else:
                saved_count += 1

    conn.commit()
    conn.close()
    return saved_count, updated_count

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
        scan_data.get('finished_at', datetime.now().isoformat()),
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
