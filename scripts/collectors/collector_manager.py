import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from scripts.collectors.remotive_collector import RemotiveCollector
from scripts.collectors.arbeitnow_collector import ArbeitnowCollector
from scripts.collectors.remoteok_collector import RemoteOKCollector
from scripts.collectors.weworkremotely_collector import WeWorkRemotelyCollector
from scripts.collectors.hackernews_collector import HackerNewsCollector
from scripts.collectors.github_bounties_collector import GitHubBountiesCollector

class CollectorManager:
    def __init__(self):
        self.collectors = [
            RemotiveCollector(),
            ArbeitnowCollector(),
            RemoteOKCollector(),
            WeWorkRemotelyCollector(),
            HackerNewsCollector(),
            GitHubBountiesCollector()
        ]

    def run_all(self):
        results = {}
        for collector in self.collectors:
            name = collector.NAME
            try:
                res = collector.collect()
                results[name] = res
            except Exception as e:
                results[name] = {
                    'success': False,
                    'source': name,
                    'items': [],
                    'error': str(e)
                }
        return results
