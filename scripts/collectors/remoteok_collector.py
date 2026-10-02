import urllib.request
import json
import os
from datetime import datetime

class RemoteOKCollector:
    NAME = 'RemoteOK'
    URL = 'https://remoteok.com/api'

    def __init__(self, timeout=25):
        self.timeout = timeout

    def collect(self, limit=75):
        req = urllib.request.Request(
            self.URL,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) RADAR-Intelligence/1.0',
                'Accept': 'application/json'
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                raw_data = json.loads(response.read().decode('utf-8'))
                # First element in RemoteOK API is metadata/legal notice
                jobs = [j for j in raw_data if isinstance(j, dict) and j.get('id')]
                if limit:
                    jobs = jobs[:limit]

                os.makedirs(r'C:\Radar\data\incoming', exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                dump_path = os.path.join(r'C:\Radar\data\incoming', f'remoteok_{timestamp}.json')
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
