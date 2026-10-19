import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from scripts.collectors.colombia_social_collector import ColombiaSocialCollector
from scripts.collectors.workana_collector import WorkanaCollector
from scripts.collectors.freelancer_collector import FreelancerCollector

class CollectorManager:
    def __init__(self):
        self.collectors = [
            ColombiaSocialCollector(),
            WorkanaCollector(),
            FreelancerCollector()
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
