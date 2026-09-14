import sys
import os
sys.path.append(r'C:\Radar')

from scripts.collectors.remotive_collector import RemotiveCollector
from scripts.collectors.arbeitnow_collector import ArbeitnowCollector
from scripts.collectors.github_bounties_collector import GitHubBountiesCollector

class CollectorManager:
    def __init__(self):
        self.collectors = [
            RemotiveCollector(),
            ArbeitnowCollector(),
            GitHubBountiesCollector()
        ]

    def run_all(self):
        results = {}
        for collector in self.collectors:
            name = collector.NAME
            res = collector.collect()
            results[name] = res
        return results
