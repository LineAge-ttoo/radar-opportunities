import urllib.request
import json
import os
from datetime import datetime

class GitHubBountiesCollector:
    NAME = 'GitHub Bounties'
    URL = 'https://api.github.com/search/issues?q=label:bounty+state:open&sort=created&order=desc&per_page=30'

    def __init__(self, timeout=25):
        self.timeout = timeout

    def collect(self, limit=30):
        req = urllib.request.Request(
            self.URL,
            headers={
                'User-Agent': 'RADAR-Intelligence/1.0 (Opportunity Discovery Engine)',
                'Accept': 'application/vnd.github.v3+json'
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode('utf-8'))
                issues = data.get('items', [])
                if limit:
                    issues = issues[:limit]

                os.makedirs(r'C:\Radar\data\incoming', exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                dump_path = os.path.join(r'C:\Radar\data\incoming', f'github_bounties_{timestamp}.json')
                with open(dump_path, 'w', encoding='utf-8') as f:
                    json.dump(issues, f, ensure_ascii=False, indent=2)

                return {
                    'success': True,
                    'source': self.NAME,
                    'items': issues,
                    'error': None
                }
        except Exception as e:
            return {
                'success': False,
                'source': self.NAME,
                'items': [],
                'error': str(e)
            }
