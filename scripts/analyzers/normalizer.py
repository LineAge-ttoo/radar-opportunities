import re
import html
import hashlib
from datetime import datetime, timezone, timedelta

def clean_html(raw_html):
    if not raw_html:
        return ''
    text = re.sub(r'<[^>]+>', ' ', str(raw_html))
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_workana_relative_date(posted_str):
    """Converts Workana strings like 'Hace 43 minutos', 'Hace 2 horas', 'Ayer' into UTC ISO-8601."""
    now = datetime.now(timezone.utc)
    s = (posted_str or '').lower().strip()
    if 'minuto' in s:
        m = re.search(r'(\d+)', s)
        mins = int(m.group(1)) if m else 15
        return (now - timedelta(minutes=mins)).isoformat()
    if 'casi una hora' in s or 'una hora' in s:
        return (now - timedelta(hours=1)).isoformat()
    if 'hora' in s:
        m = re.search(r'(\d+)', s)
        hrs = int(m.group(1)) if m else 2
        return (now - timedelta(hours=hrs)).isoformat()
    if 'ayer' in s:
        return (now - timedelta(hours=24)).isoformat()
    if 'día' in s or 'dia' in s:
        m = re.search(r'(\d+)', s)
        days = int(m.group(1)) if m else 2
        return (now - timedelta(days=days)).isoformat()
    return (now - timedelta(hours=3)).isoformat()

def parse_workana_budget(budget_str):
    if not budget_str:
        return None, None, 'USD'
    s = str(budget_str).strip()
    curr = 'COP' if 'COP' in s.upper() else ('EUR' if 'EUR' in s.upper() else 'USD')
    nums = []
    for m in re.findall(r'\d+(?:[\.,]\d+)?', s):
        clean_m = m.replace('.', '').replace(',', '.')
        try:
            nums.append(float(clean_m))
        except ValueError:
            pass
    if not nums:
        return None, None, curr
    if len(nums) == 1:
        return nums[0], nums[0], curr
    return min(nums), max(nums), curr

class OpportunityNormalizer:
    @staticmethod
    def normalize_colombia_social(item):
        now_iso = datetime.now(timezone.utc).isoformat()
        url = item.get('url', '')
        opp_id = f"co_social_{hashlib.md5(url.encode()).hexdigest()[:12]}"

        platform = item.get('platform', 'Instagram Colombia')
        biz_name = item.get('business_name', 'Negocio en Colombia')
        offer_type = item.get('offer_type', 'whatsapp_bot')
        niche = item.get('niche', 'Cliente Potencial Colombia')
        cop_min = float(item.get('cop_min', 250000))
        cop_max = float(item.get('cop_max', 850000))
        wa_phone = item.get('whatsapp_phone')

        if offer_type == 'bioconstruccion_guadua':
            action_title = f"🎋 Cabañas en Guadua, Muro Tendinoso & Vidrio para: {biz_name}"
        elif offer_type == 'metal_soldadura':
            action_title = f"🔩 Estructuras en Metal, Soldadura & Remodelación para: {biz_name}"
        elif offer_type == 'informales_manualidades':
            action_title = f"🛠️ [2do Tiempo & Manualidades] Lámparas, Vidrio y Guadua para: {biz_name}"
        elif offer_type == 'planos_3d':
            action_title = f"📐 Hacer Planos / Render 3D y Remodelación para: {biz_name}"
        elif offer_type == 'whatsapp_bot':
            action_title = f"🤖 Automatizar WhatsApp / Citas para: {biz_name}"
        else:
            action_title = f"🌐 Crear Catálogo Digital / Web para: {biz_name}"

        desc = f"{item.get('service_pitch', '')} | Perfil detectado en {platform}: {item.get('snippet', '')}"
        if wa_phone:
            desc = f"📱 WhatsApp Directo Detectado: +{wa_phone} | " + desc

        approx_place = item.get('approx_place') or f"Perfil activo en {platform} (Colombia)"
        contractor_info = item.get('contractor_info') or f"Contratante / Negocio: {biz_name} en {platform}. {item.get('snippet', '')[:160]}"

        return {
            'opportunity_id': opp_id,
            'source': platform,
            'source_url': url,
            'discovered_at': now_iso,
            'published_at': now_iso,
            'title': action_title,
            'organization': f"{biz_name} (🇨🇴 Colombia)",
            'description': desc,
            'category': niche,
            'opportunity_type': 'cliente_directo_colombia',
            'payment_min': cop_min,
            'payment_max': cop_max,
            'currency': 'COP',
            'location': 'Colombia',
            'approx_place': approx_place,
            'contractor_info': contractor_info,
            'remote': True,
            'skills': item.get('skills', ['automatizacion', 'whatsapp', 'planos', '3d']),
            'contact_phone': f"+{wa_phone}" if wa_phone and not str(wa_phone).startswith('+') else (wa_phone or ''),
            'contact_whatsapp_url': f"https://wa.me/{str(wa_phone).replace('+','').replace(' ','')}" if wa_phone else '',
            'raw_data': item,
            'observed_data': {
                'stated_salary': f"COP ${int(cop_min):,} - ${int(cop_max):,}".replace(',', '.'),
                'stated_location': '🇨🇴 Colombia',
                'stated_job_type': 'Cliente Directo (Sin Contrato Legal)',
                'whatsapp_phone': wa_phone,
                'approx_place': approx_place,
                'contractor_info': contractor_info,
                'offer_type': offer_type,
                'category_hint': offer_type,
                'tags': item.get('skills', []) + ['colombia', platform.lower()]
            }
        }

    @staticmethod
    def normalize_workana(item):
        now_iso = datetime.now(timezone.utc).isoformat()
        slug = item.get('slug', '')
        url = f"https://www.workana.com/job/{slug}" if slug else "https://www.workana.com/jobs?country=CO"
        opp_id = f"workana_{hashlib.md5(slug.encode()).hexdigest()[:12]}"

        clean_title = clean_html(item.get('title', ''))
        clean_desc = clean_html(item.get('description', ''))
        country_raw = clean_html(item.get('country', '')) or ('Colombia' if item.get('is_colombia_search') else 'Latinoamérica')
        if item.get('is_colombia_search') or 'colombia' in country_raw.lower():
            country_display = '🇨🇴 Colombia'
        else:
            country_display = country_raw

        budget_str = clean_html(item.get('budget', ''))
        p_min, p_max, curr = parse_workana_budget(budget_str)
        pub_iso = parse_workana_relative_date(item.get('postedDate', ''))

        skills_list = []
        for sk in (item.get('skills') or []):
            if isinstance(sk, dict) and sk.get('anchorText'):
                skills_list.append(sk['anchorText'])
            elif isinstance(sk, str):
                skills_list.append(sk)

        return {
            'opportunity_id': opp_id,
            'source': 'Workana Colombia' if 'Colombia' in country_display else 'Workana (Español)',
            'source_url': url,
            'discovered_at': now_iso,
            'published_at': pub_iso,
            'title': clean_title,
            'organization': f"Cliente {item.get('authorName') or 'Workana'} ({country_display})",
            'description': clean_desc,
            'category': item.get('radar_search_label', 'Tarea Freelance'),
            'opportunity_type': 'tarea_directa',
            'payment_min': p_min,
            'payment_max': p_max,
            'currency': curr,
            'location': country_display,
            'remote': True,
            'raw_data': {
                'slug': slug,
                'postedDate': item.get('postedDate'),
                'totalBids': item.get('totalBids')
            },
            'observed_data': {
                'stated_salary': budget_str or 'Por cotizar',
                'stated_location': country_display,
                'stated_job_type': f"Proyecto Corto ({item.get('postedDate', 'Hoy')})",
                'tags': skills_list
            }
        }

    @staticmethod
    def normalize_freelancer(item):
        now_iso = datetime.now(timezone.utc).isoformat()
        pid = str(item.get('id', ''))
        seo_url = item.get('seo_url', '')
        url = f"https://www.freelancer.co/projects/{seo_url}" if seo_url else f"https://www.freelancer.co/projects/{pid}"
        opp_id = f"fl_{pid}"

        title = clean_html(item.get('title', ''))
        desc = clean_html(item.get('description') or item.get('preview_description') or '')
        budget = item.get('budget') or {}
        p_min = budget.get('minimum')
        p_max = budget.get('maximum')
        curr = (item.get('currency') or {}).get('code') or 'USD'

        submit_ts = item.get('submitdate') or item.get('time_submitted')
        if submit_ts:
            pub_iso = datetime.fromtimestamp(float(submit_ts), tz=timezone.utc).isoformat()
        else:
            pub_iso = now_iso

        jobs = [j.get('name', '') for j in (item.get('jobs') or []) if isinstance(j, dict) and j.get('name')]
        stated_sal = f"{curr} {int(p_min):,} - {int(p_max):,}" if (p_min and p_max) else None

        return {
            'opportunity_id': opp_id,
            'source': 'Freelancer.co',
            'source_url': url,
            'discovered_at': now_iso,
            'published_at': pub_iso,
            'title': title,
            'organization': f"Proyecto Directo ({item.get('radar_category_label', 'Freelance')})",
            'description': desc,
            'category': item.get('radar_category_label', 'Tareas & Diseño'),
            'opportunity_type': 'tarea_directa',
            'payment_min': p_min,
            'payment_max': p_max,
            'currency': curr,
            'location': 'Remoto (Sin Contrato Legal)',
            'remote': True,
            'raw_data': {
                'id': pid,
                'seo_url': seo_url,
                'bid_count': (item.get('bid_stats') or {}).get('bid_count')
            },
            'observed_data': {
                'stated_salary': stated_sal,
                'stated_location': 'Colombia / Internacional',
                'stated_job_type': 'Pago por Tarea / Entregable',
                'tags': jobs
            }
        }

    @staticmethod
    def normalize_san_agustin_huila(item):
        now_iso = datetime.now(timezone.utc).isoformat()
        opp_id = item.get('id') or f"huila_{hashlib.md5(str(item.get('url','')).encode()).hexdigest()[:10]}"
        p_min = float(item.get('budget_min', 250000))
        p_max = float(item.get('budget_max', 2500000))
        curr = item.get('currency', 'COP')
        stated_sal = f"{curr} ${int(p_min):,} — ${int(p_max):,}".replace(',', '.')
        loc = item.get('location', '📍 San Agustín, Huila')
        skills = item.get('skills', ['San Agustín Huila', 'Guadua & Cabañas', 'Blender 3D'])

        return {
            'opportunity_id': opp_id,
            'source': 'San Agustín · Huila · Guadua',
            'source_url': item.get('url', 'https://www.sanagustin-huila.gov.co/contratacion'),
            'discovered_at': now_iso,
            'published_at': item.get('published_at') or now_iso,
            'title': item.get('title', 'Proyecto San Agustín Huila'),
            'organization': item.get('organization', 'San Agustín Huila'),
            'description': item.get('description', ''),
            'category': item.get('category_hint', 'guadua_cabanas'),
            'opportunity_type': 'san_agustin_huila_prioridad',
            'payment_min': p_min,
            'payment_max': p_max,
            'currency': curr,
            'location': loc,
            'approx_place': item.get('approx_place') or loc,
            'contractor_info': item.get('contractor_info') or f"Contratante verificado: {item.get('organization', 'San Agustín Huila')}",
            'lat': item.get('lat', 1.8792),
            'lon': item.get('lon', -76.2706),
            'distance_km': item.get('distance_km', 0.5),
            'remote': True,
            'skills': skills,
            'contact_phone': item.get('contact_phone') or item.get('whatsapp_phone') or '',
            'contact_whatsapp_url': item.get('contact_whatsapp_url') or '',
            'circular_code': item.get('circular_code') or '',
            'contact_email': item.get('contact_email') or '',
            'raw_data': item,
            'observed_data': {
                'stated_salary': stated_sal,
                'stated_location': loc,
                'stated_job_type': 'Prioridad Zona San Agustín / Huila',
                'whatsapp_phone': item.get('whatsapp_phone') or '',
                'contact_phone': item.get('contact_phone') or item.get('whatsapp_phone') or '',
                'contact_whatsapp_url': item.get('contact_whatsapp_url') or '',
                'circular_code': item.get('circular_code') or '',
                'contact_email': item.get('contact_email') or '',
                'approx_place': item.get('approx_place') or loc,
                'contractor_info': item.get('contractor_info') or f"Contratante verificado: {item.get('organization', 'San Agustín Huila')}",
                'lat': item.get('lat', 1.8792),
                'lon': item.get('lon', -76.2706),
                'distance_km': item.get('distance_km', 0.5),
                'category_hint': item.get('category_hint', 'guadua_cabanas'),
                'tags': skills + ['san agustin', 'huila', 'guadua', 'bioconstruccion', 'muro tendinoso', 'metal', 'soldadura', 'blender', 'estudiantes']
            }
        }

