import urllib.request
import urllib.parse
import json
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

class FreelancerCollector:
    NAME = 'Freelancer.co (Tareas & Proyectos)'
    BASE_API = 'https://www.freelancer.com/api/projects/0.1/projects/active/'

    QUERIES = [
        ('Tareas en Español', 'languages[]=es&limit=30&full_description=true&job_details=true'),
        ('Planos, AutoCAD & 3D', 'query=autocad%20planos%203d%20render%20blender&limit=25&full_description=true&job_details=true'),
        ('Bots, WhatsApp & Automatización', 'query=whatsapp%20bot%20automatizacion%20n8n%20automation&limit=25&full_description=true&job_details=true'),
        ('Páginas Web & Catálogos ES', 'query=pagina%20web%20landing%20catalogo%20diseño&languages[]=es&limit=25&full_description=true&job_details=true')
    ]

    def __init__(self, timeout=20):
        self.timeout = timeout

    def collect(self, limit=80):
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        seen_ids = set()
        all_projects = []
        errors = []

        for label, q_params in self.QUERIES:
            url = f"{self.BASE_API}?{q_params}"
            req = urllib.request.Request(url, headers={'User-Agent': ua, 'Accept': 'application/json'})
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    data = json.loads(response.read().decode('utf-8', errors='ignore'))
                    projects = data.get('result', {}).get('projects', [])
                    for p in projects:
                        pid = p.get('id')
                        if not pid or pid in seen_ids:
                            continue
                        # Skip overly massive enterprise projects > $4000 USD
                        b_max = (p.get('budget') or {}).get('maximum') or 0
                        if b_max > 4000 and p.get('currency', {}).get('code') in ['USD', 'EUR', 'GBP']:
                            continue
                        seen_ids.add(pid)
                        p['radar_category_label'] = label
                        all_projects.append(p)
            except Exception as e:
                errors.append(f"{label}: {str(e)}")

        all_projects = all_projects[:limit]

        try:
            incoming_dir = os.path.join(BASE_DIR, 'data', 'incoming')
            os.makedirs(incoming_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            dump_path = os.path.join(incoming_dir, f'freelancer_{timestamp}.json')
            with open(dump_path, 'w', encoding='utf-8') as f:
                json.dump(all_projects, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

        return {
            'success': len(all_projects) > 0,
            'source': self.NAME,
            'items': all_projects,
            'error': '; '.join(errors) if (errors and not all_projects) else None
        }
