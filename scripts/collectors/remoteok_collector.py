import urllib.request
import json
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

class RemoteOKCollector:
    NAME = 'RemoteOK'
    URL = 'https://remoteok.com/api'

    def __init__(self, timeout=25):
        self.timeout = timeout

    def collect(self, limit=80):
        req = urllib.request.Request(
            self.URL,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) RADAR-Intelligence/2.0',
                'Accept': 'application/json'
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                raw_data = json.loads(response.read().decode('utf-8'))
                jobs = [j for j in raw_data if isinstance(j, dict) and j.get('id')]
                if limit:
                    jobs = jobs[:limit]

                try:
                    incoming_dir = os.path.join(BASE_DIR, 'data', 'incoming')
                    os.makedirs(incoming_dir, exist_ok=True)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    dump_path = os.path.join(incoming_dir, f'remoteok_{timestamp}.json')
                    with open(dump_path, 'w', encoding='utf-8') as f:
                        json.dump(jobs, f, ensure_ascii=False, indent=2)
                except Exception:
                    pass

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
