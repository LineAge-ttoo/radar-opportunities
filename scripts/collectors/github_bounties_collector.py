import urllib.request
import json
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

class GitHubBountiesCollector:
    NAME = 'GitHub Bounties'
    URLS = [
        'https://api.github.com/search/issues?q=label:bounty+state:open+is:issue&sort=created&order=desc&per_page=35',
        'https://api.github.com/search/issues?q=%22bounty%22+%22$%22+state:open+is:issue&sort=created&order=desc&per_page=25'
    ]

    def __init__(self, timeout=25):
        self.timeout = timeout

    def collect(self, limit=50):
        seen_ids = set()
        all_issues = []
        errors = []

        for url in self.URLS:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'RADAR-Intelligence/2.0 (Opportunity Discovery Engine)',
                    'Accept': 'application/vnd.github.v3+json'
                }
            )
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    data = json.loads(response.read().decode('utf-8'))
                    for issue in data.get('items', []):
                        iid = issue.get('id')
                        if iid and iid not in seen_ids:
                            seen_ids.add(iid)
                            all_issues.append(issue)
            except Exception as e:
                errors.append(str(e))

        if limit:
            all_issues = all_issues[:limit]

        try:
            incoming_dir = os.path.join(BASE_DIR, 'data', 'incoming')
            os.makedirs(incoming_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            dump_path = os.path.join(incoming_dir, f'github_bounties_{timestamp}.json')
            with open(dump_path, 'w', encoding='utf-8') as f:
                json.dump(all_issues, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

        return {
            'success': len(all_issues) > 0,
            'source': self.NAME,
            'items': all_issues,
            'error': '; '.join(errors) if (errors and not all_issues) else None
        }
