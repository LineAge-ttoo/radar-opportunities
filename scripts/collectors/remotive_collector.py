import urllib.request
import json
import os
from datetime import datetime

class RemotiveCollector:
    NAME = 'Remotive'
    URL = 'https://remotive.com/api/remote-jobs'

    def __init__(self, timeout=25):
        self.timeout = timeout

    def collect(self, limit=None):
        req = urllib.request.Request(
            self.URL,
            headers={
                'User-Agent': 'RADAR-Intelligence/1.0 (Opportunity Discovery Engine)',
                'Accept': 'application/json'
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode('utf-8'))
                jobs = data.get('jobs', [])
                if limit:
                    jobs = jobs[:limit]

                os.makedirs(r'C:\Radar\data\incoming', exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                dump_path = os.path.join(r'C:\Radar\data\incoming', f'remotive_{timestamp}.json')
                with open(dump_path, 'w', encoding='utf-8') as f:
                    json.dump(jobs, f, ensure_ascii=False, indent=2)

                return {
                    'success': True,
                    'source': self.NAME,
                    'items': jobs,
                    'error': None
                }
        except Exception as e:
            return {
                'success': False,
                'source': self.NAME,
                'items': [],
                'error': str(e)
            }
