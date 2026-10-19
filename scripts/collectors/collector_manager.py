from .san_agustin_huila_collector import SanAgustinHuilaCollector
from .colombia_social_collector import ColombiaSocialCollector
from .workana_collector import WorkanaCollector
from .freelancer_collector import FreelancerCollector


class CollectorManager:
    def __init__(self):
        self.collectors = [
            SanAgustinHuilaCollector(),
            ColombiaSocialCollector(),
            WorkanaCollector(),
            FreelancerCollector()
        ]

    def run_all(self) -> dict:
        results = {}
        for c in self.collectors:
            source_name = getattr(c, 'NAME', c.__class__.__name__)
            try:
                res = c.collect()
                results[source_name] = res
            except Exception as e:
                results[source_name] = {
                    "success": False,
                    "error": str(e),
                    "items": []
                }
        return results
