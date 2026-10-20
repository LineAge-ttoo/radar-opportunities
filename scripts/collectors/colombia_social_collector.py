import urllib.request
import urllib.parse
import json
import os
import glob
import re
import html
import time
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def extract_colombia_phone(text):
    """Extracts Colombian mobile/WhatsApp numbers (e.g. +57 314 585 2140 or 3152773906) from text."""
    if not text:
        return None
    m = re.search(r'(?:\+?57[\s\-\.]?)?(3\d{2}[\s\-\.]?\d{3}[\s\-\.]?\d{4})\b', text)
    if m:
        digits = re.sub(r'\D', '', m.group(1))
        if len(digits) == 10 and digits.startswith('3'):
            return '57' + digits
    return None

class ColombiaSocialCollector:
    NAME = 'Clientes Colombia (Instagram & Facebook)'
    DDG_URL = 'https://html.duckduckgo.com/html/?q='

    SEARCH_CAMPAIGNS = [
        {
            'niche': '🎋 Bioconstrucción, Guadua, Muro Tendinoso & Glampings (Redes Colombia)',
            'query': 'site:instagram.com OR site:facebook.com colombia bioconstruccion guadua cabanas glamping whatsapp',
            'platform': 'Grupos & Redes Colombia',
            'offer_type': 'bioconstruccion_guadua',
            'cop_min': 650000,
            'cop_max': 4500000,
            'skills': ['bioconstrucción', 'muro tendinoso', 'guadua', 'botellas & vidrio'],
            'service_pitch': 'Construcción y remodelación de cabañas con muro tendinoso, incrustaciones de botellas, muros en vidrio, acabados en guadua certificada y renders 3D.'
        },
        {
            'niche': '🔩 Estructuras Metálicas, Soldadura & Remodelaciones (Grupos & Redes Colombia)',
            'query': 'site:facebook.com OR site:instagram.com colombia estructuras metalicas soldadura cubiertas remodelaciones whatsapp',
            'platform': 'Facebook & Instagram Colombia',
            'offer_type': 'metal_soldadura',
            'cop_min': 350000,
            'cop_max': 3200000,
            'skills': ['estructuras en metal', 'soldadura', 'remodelación', 'guadua & metal'],
            'service_pitch': 'Fabricación, soldadura y remodelación de estructuras metálicas, cubiertas mixtas en metal y guadua, pérgolas, portones y planos 3D.'
        },
        {
            'niche': '🛠️ Manualidades, Artesanías en Guadua/Vidrio & 2do Tiempo (Redes Colombia)',
            'query': 'site:instagram.com OR site:facebook.com colombia artesanias guadua bambu lamparas decoracion rustica whatsapp',
            'platform': 'Redes & Grupos Colombia',
            'offer_type': 'informales_manualidades',
            'cop_min': 90000,
            'cop_max': 650000,
            'skills': ['manualidades', '2do tiempo', 'lámparas guadua', 'vidrio & metal'],
            'service_pitch': 'Elaboración por encargo de lámparas en guadua, decoración con botellas de vidrio, muebles rústicos en metal/bambú y reparaciones locativas.'
        },
        {
            'niche': '📐 Planos, Renders 3D & Remodelaciones (Instagram Colombia)',
            'query': 'site:instagram.com colombia remodelaciones arquitectura diseno interior whatsapp',
            'platform': 'Instagram Colombia',
            'offer_type': 'planos_3d',
            'cop_min': 250000,
            'cop_max': 950000,
            'skills': ['planos', '3d / render', 'autocad', 'diseño interior'],
            'service_pitch': 'Elaboración de planos 2D/3D, distribución de espacios y renders fotorrealistas para que cierren más obras y remodelaciones con sus clientes.'
        },
        {
            'niche': '🌐 Web Interactiva & Reservas para Glampings y Hoteles (Instagram Colombia)',
            'query': 'site:instagram.com colombia glamping cabanas reservas whatsapp huila antioquia',
            'platform': 'Instagram Colombia',
            'offer_type': 'web_catalogo',
            'cop_min': 350000,
            'cop_max': 1200000,
            'skills': ['web / catálogo', 'whatsapp / bot', 'automatización'],
            'service_pitch': 'Página web interactiva con catálogo de cabañas, precios claros y botón de reserva automatizada directo a WhatsApp.'
        }
    ]

    def __init__(self, timeout=18):
        self.timeout = timeout

    def load_cached_social_leads(self, seen_urls):
        cached = []
        incoming_dir = os.path.join(BASE_DIR, 'data', 'incoming')
        for fpath in sorted(glob.glob(os.path.join(incoming_dir, 'colombia_social_*.json')), reverse=True):
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    items = json.load(f)
                for it in items:
                    u = it.get('url')
                    if u and u not in seen_urls:
                        seen_urls.add(u)
                        if not it.get('whatsapp_phone'):
                            it['whatsapp_phone'] = extract_colombia_phone(f"{it.get('title', '')} {it.get('snippet', '')}")
                        if not it.get('skills'):
                            it['skills'] = ['planos', '3d / render', 'whatsapp / bot'] if it.get('offer_type') == 'planos_3d' else ['whatsapp / bot', 'automatización', 'web / catálogo']
                        cached.append(it)
            except Exception:
                pass
        return cached

    def collect(self, limit=60):
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        seen_urls = set()
        all_leads = self.load_cached_social_leads(seen_urls)
        errors = []

        block_re = re.compile(
            r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?class="result__snippet"[^>]*>(.*?)</a>',
            re.S
        )

        for idx, camp in enumerate(self.SEARCH_CAMPAIGNS):
            if idx > 0:
                time.sleep(1.2)
            url = self.DDG_URL + urllib.parse.quote(camp['query'])
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': ua,
                    'Accept-Language': 'es-CO,es;q=0.9'
                }
            )
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    raw_html = response.read().decode('utf-8', errors='ignore')
                    matches = block_re.findall(raw_html)
                    for raw_href, raw_title, raw_snippet in matches[:8]:
                        if 'uddg=' in raw_href:
                            real_url = urllib.parse.unquote(raw_href.split('uddg=')[-1].split('&')[0])
                        else:
                            real_url = raw_href

                        if not real_url.startswith('http') or real_url in seen_urls:
                            continue
                        seen_urls.add(real_url)

                        clean_title = html.unescape(re.sub(r'<[^>]+>', '', raw_title)).strip()
                        clean_snippet = html.unescape(re.sub(r'<[^>]+>', '', raw_snippet)).strip()

                        biz_name = clean_title.split('•')[0].split('|')[0].split(' - ')[0].strip()
                        if len(biz_name) > 55 or not biz_name:
                            biz_name = clean_title[:50]

                        phone_co = extract_colombia_phone(f"{clean_title} {clean_snippet}")

                        all_leads.append({
                            'url': real_url,
                            'title': clean_title,
                            'business_name': biz_name,
                            'snippet': clean_snippet,
                            'niche': camp['niche'],
                            'platform': camp['platform'],
                            'offer_type': camp['offer_type'],
                            'cop_min': camp['cop_min'],
                            'cop_max': camp['cop_max'],
                            'skills': camp['skills'],
                            'service_pitch': camp['service_pitch'],
                            'whatsapp_phone': phone_co
                        })
            except Exception as e:
                errors.append(f"{camp['niche']}: {str(e)}")

        all_leads = all_leads[:limit]

        if all_leads:
            try:
                incoming_dir = os.path.join(BASE_DIR, 'data', 'incoming')
                os.makedirs(incoming_dir, exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                dump_path = os.path.join(incoming_dir, f'colombia_social_{timestamp}.json')
                with open(dump_path, 'w', encoding='utf-8') as f:
                    json.dump(all_leads, f, ensure_ascii=False, indent=2)
            except Exception:
                pass

        return {
            'success': len(all_leads) > 0,
            'source': self.NAME,
            'items': all_leads,
            'error': '; '.join(errors) if (errors and not all_leads) else None
        }
