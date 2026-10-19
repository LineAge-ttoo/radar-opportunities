import urllib.request
import urllib.parse
import json
import os
import re
import html
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

class WorkanaCollector:
    NAME = 'Workana Colombia & LATAM'
    URLS = [
        ('Colombia Directo', 'https://www.workana.com/jobs?country=CO'),
        ('Automatización & Bots', 'https://www.workana.com/jobs?language=es&query=automatizacion+whatsapp+bot+n8n'),
        ('Planos, CAD & 3D', 'https://www.workana.com/jobs?language=es&query=planos+autocad+3d+render+blender'),
        ('Web, Catálogos & Diseño', 'https://www.workana.com/jobs?language=es&query=landing+page+catalogo+diseno+web'),
        ('Tareas Recientes ES', 'https://www.workana.com/jobs?language=es')
    ]

    def __init__(self, timeout=20):
        self.timeout = timeout

    def collect(self, limit=60):
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        seen_slugs = set()
        all_items = []
        errors = []

        for label, url in self.URLS:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': ua,
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept-Language': 'es-CO,es;q=0.9'
                }
            )
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    data = json.loads(response.read().decode('utf-8', errors='ignore'))
                    results = data.get('results', {}).get('results', [])
                    for item in results:
                        slug = item.get('slug')
                        if not slug or slug in seen_slugs:
                            continue
                        seen_slugs.add(slug)
                        item['radar_search_label'] = label
                        item['is_colombia_search'] = ('country=CO' in url)
                        all_items.append(item)
            except Exception as e:
                errors.append(f"{label}: {str(e)}")

        all_items = all_items[:limit]

        try:
            incoming_dir = os.path.join(BASE_DIR, 'data', 'incoming')
            os.makedirs(incoming_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            dump_path = os.path.join(incoming_dir, f'workana_{timestamp}.json')
            with open(dump_path, 'w', encoding='utf-8') as f:
                json.dump(all_items, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

        return {
            'success': len(all_items) > 0,
            'source': self.NAME,
            'items': all_items,
            'error': '; '.join(errors) if (errors and not all_items) else None
        }
