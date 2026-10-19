import urllib.request
import urllib.parse
import json
import os
import time
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

class HackerNewsCollector:
    NAME = 'HackerNews'
    BASE_URL = 'https://hn.algolia.com/api/v1/search_by_date'

    def __init__(self, timeout=20):
        self.timeout = timeout

    def collect(self, limit=60):
        # Only fetch items from the last 30 days so every opportunity is fresh
        thirty_days_ago = int(time.time()) - (30 * 86400)
        queries = [
            f"{self.BASE_URL}?tags=job&numericFilters=created_at_i>{thirty_days_ago}&hitsPerPage=25",
            f"{self.BASE_URL}?query=freelance+remote&tags=comment&numericFilters=created_at_i>{thirty_days_ago}&hitsPerPage=20",
            f"{self.BASE_URL}?query=hiring+remote+contract&tags=comment&numericFilters=created_at_i>{thirty_days_ago}&hitsPerPage=20",
            f"{self.BASE_URL}?query=automation+python+api&tags=comment&numericFilters=created_at_i>{thirty_days_ago}&hitsPerPage=15"
        ]

        seen_ids = set()
        all_hits = []
        errors = []

        for url in queries:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (RADAR Intelligence Engine/2.0)'}
            )
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    for hit in data.get('hits', []):
                        oid = str(hit.get('objectID', ''))
                        if oid and oid not in seen_ids:
                            seen_ids.add(oid)
                            all_hits.append(hit)
            except Exception as e:
                errors.append(str(e))

        all_hits = all_hits[:limit]

        try:
            incoming_dir = os.path.join(BASE_DIR, 'data', 'incoming')
            os.makedirs(incoming_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            dump_path = os.path.join(incoming_dir, f'hackernews_{timestamp}.json')
            with open(dump_path, 'w', encoding='utf-8') as f:
                json.dump(all_hits, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

        return {
            'success': len(all_hits) > 0,
            'source': self.NAME,
            'items': all_hits,
            'error': '; '.join(errors) if (errors and not all_hits) else None
        }
