import urllib.request
import json
import os
from datetime import datetime

class HackerNewsCollector:
    NAME = 'HackerNews'
    BASE_URL = 'https://hn.algolia.com/api/v1/search_by_date'

    def __init__(self, timeout=25):
        self.timeout = timeout

    def collect(self, limit=30):
        # Query for recent comments offering freelance/contract/automation work
        query = 'hiring+OR+contract+OR+freelance+OR+automation'
        url = f"{self.BASE_URL}?query={query}&tags=comment&hitsPerPage={limit}"
        
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (RADAR Intelligence Engine)'}
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode('utf-8'))
                hits = data.get('hits', [])

                os.makedirs(r'C:\Radar\data\incoming', exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                dump_path = os.path.join(r'C:\Radar\data\incoming', f'hackernews_{timestamp}.json')
                with open(dump_path, 'w', encoding='utf-8') as f:
                    json.dump(hits, f, ensure_ascii=False, indent=2)

                return {
                    'success': True,
                    'source': self.NAME,
                    'items': hits,
                    'error': None
                }
        except Exception as e:
            return {
                'success': False,
                'source': self.NAME,
                'items': [],
                'error': str(e)
            }
