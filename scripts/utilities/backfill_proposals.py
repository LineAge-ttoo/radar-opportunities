import sqlite3
import json
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from scripts.utilities.db import get_all_opportunities, get_stats, DEFAULT_DB_PATH

def clean_and_sync():
    conn = sqlite3.connect(DEFAULT_DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM opportunities WHERE last_seen_at < '2026-10-19';")
    deleted = cur.rowcount
    conn.commit()
    conn.close()
    print(f"Purged {deleted} stale records from before 2026-10-19.")

    stats = get_stats()
    opps = get_all_opportunities(limit=250)

    for path in [
        os.path.join(BASE_DIR, 'data', 'opportunities', 'latest_scan.json'),
        os.path.join(BASE_DIR, 'app', 'latest_scan.json')
    ]:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data['stats'] = stats
            data['opportunities'] = opps
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    print("Stats after cleanup:", stats)
    print(f"Synced {len(opps)} actionable fresh opportunities to JSON snapshots.")

if __name__ == '__main__':
    clean_and_sync()
