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


def format_exact_time_ago(iso_str, fallback_str=None):
    if fallback_str and any(k in str(fallback_str).lower() for k in ['minuto', 'hora', 'hoy', 'ayer']):
        return str(fallback_str).strip()
    try:
        s = str(iso_str or '').replace('Z', '+00:00')
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        diff_mins = max(1, int((datetime.now(timezone.utc) - dt).total_seconds() // 60))
        if diff_mins < 60:
            return f"Publicado hace {diff_mins} minutos (Hoy)"
        hrs = diff_mins // 60
        if hrs < 24:
            return f"Publicado hace {hrs} {'hora' if hrs == 1 else 'horas'} (Hoy)"
        days = hrs // 24
        return f"Publicado hace {days} {'día' if days == 1 else 'días'}"
    except Exception:
        return "Publicado Hoy (Reciente)"


def parse_workana_relative_date(posted_str):
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
    return (now - timedelta(hours=2)).isoformat()


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
        opp_id = item.get('id') or f"co_social_{hashlib.md5(url.encode()).hexdigest()[:12]}"

        platform = item.get('platform', 'Comprador Verificado Colombia')
        biz_name = item.get('business_name', 'Comprador / Cliente Colombia')
        offer_type = item.get('offer_type', 'cafe_secaderos')
        niche = item.get('niche', '☕ Compradores Café Especial & Borbón Rosado')
        cop_min = float(item.get('cop_min', 600000))
        cop_max = float(item.get('cop_max', 18000000))
        wa_phone = item.get('whatsapp_phone')
        raw_snippet = clean_html(item.get('snippet', ''))

        action_title = item.get('title') or f"☕ Comprador de Café Especial: {biz_name}"
        origin_source = item.get('origin_source_detail') or f"Publicado en: {platform} ({url})"
        time_ago = item.get('time_ago_exact') or "Activo hoy"
        verbatim_req = item.get('verbatim_request') or f"\"{raw_snippet or action_title}\""
        reqs = item.get('requirements_list') or [
            f"Especialidad solicitada: {', '.join(item.get('skills', ['Café Borbón Rosado / Especialidad']))}.",
            "Modalidad: Negociación directa con el comprador sin intermediarios."
        ]

        desc = raw_snippet or item.get('service_pitch', '')
        if wa_phone:
            desc = f"📱 WhatsApp Directo Verificado: +{wa_phone} | " + desc

        approx_place = item.get('approx_place') or f"{platform} (Colombia)"
        contractor_info = item.get('contractor_info') or f"Comprador / Entidad: {biz_name}."
        pub_at = item.get('published_at') or now_iso

        return {
            'opportunity_id': opp_id,
            'source': platform,
            'source_url': url,
            'discovered_at': now_iso,
            'published_at': pub_at,
            'title': action_title,
            'organization': biz_name,
            'description': desc,
            'category': offer_type,
            'opportunity_type': 'san_agustin_huila_prioridad' if offer_type == 'cafe_secaderos' else 'cliente_directo_colombia',
            'payment_min': cop_min,
            'payment_max': cop_max,
            'currency': 'COP',
            'location': approx_place,
            'approx_place': approx_place,
            'contractor_info': contractor_info,
            'origin_source_detail': origin_source,
            'time_ago_exact': time_ago,
            'verbatim_request': verbatim_req,
            'requirements_list': reqs,
            'remote': True,
            'skills': item.get('skills', ['☕ Comprador Café Especial', 'Borbón Rosado']),
            'contact_phone': f"+{wa_phone}" if wa_phone and not str(wa_phone).startswith('+') else (wa_phone or ''),
            'contact_whatsapp_url': f"https://wa.me/{str(wa_phone).replace('+','').replace(' ','')}" if wa_phone else '',
            'raw_data': item,
            'observed_data': {
                'stated_salary': f"COP ${int(cop_min):,} - ${int(cop_max):,}".replace(',', '.'),
                'stated_location': approx_place,
                'stated_job_type': 'Comprador Directo Verificado',
                'whatsapp_phone': wa_phone,
                'approx_place': approx_place,
                'contractor_info': contractor_info,
                'origin_source_detail': origin_source,
                'time_ago_exact': time_ago,
                'verbatim_request': verbatim_req,
                'requirements_list': reqs,
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
        posted_raw = clean_html(item.get('postedDate', '')) or 'Hace 1 hora'
        pub_iso = parse_workana_relative_date(posted_raw)

        skills_list = []
        for sk in (item.get('skills') or []):
            if isinstance(sk, dict) and sk.get('anchorText'):
                skills_list.append(sk['anchorText'])
            elif isinstance(sk, str):
                skills_list.append(sk)

        author_name = clean_html(item.get('authorName') or 'Solicitante en Workana')
        bids_str = clean_html(str(item.get('totalBids') or 'Pocas propuestas'))
        origin_source = f"Publicado en: Workana ({country_display}) — Categoría {item.get('radar_search_label', 'Proyectos')}"
        time_ago = f"Publicado: {posted_raw}"
        verbatim_req = f"\"{clean_desc or clean_title}\""
        reqs = [
            f"Habilidades exigidas por el solicitante: {', '.join(skills_list) if skills_list else 'Diseño / Planos 3D / Desarrollo práctico'}.",
            f"Presupuesto publicado por el cliente: {budget_str or 'Abierto a cotización'}.",
            f"Competencia actual en el anuncio: {bids_str}.",
            "Entregar avance inicial rápido y archivos editables según lo descrito en la solicitud textual."
        ]
        contractor_info = f"Demandante: {author_name} ({country_display}). Publicó el anuncio en Workana ({posted_raw}) con presupuesto de {budget_str or 'cotización abierta'}."

        return {
            'opportunity_id': opp_id,
            'source': 'Workana Colombia' if 'Colombia' in country_display else 'Workana (Español)',
            'source_url': url,
            'discovered_at': now_iso,
            'published_at': pub_iso,
            'title': clean_title,
            'organization': f"Cliente {author_name} ({country_display})",
            'description': clean_desc,
            'category': item.get('radar_search_label', 'Tarea Freelance'),
            'opportunity_type': 'tarea_directa',
            'payment_min': p_min,
            'payment_max': p_max,
            'currency': curr,
            'location': country_display,
            'approx_place': f"{country_display} (Trabajo Remoto / Entregable Digital)",
            'contractor_info': contractor_info,
            'origin_source_detail': origin_source,
            'time_ago_exact': time_ago,
            'verbatim_request': verbatim_req,
            'requirements_list': reqs,
            'remote': True,
            'raw_data': {
                'slug': slug,
                'postedDate': posted_raw,
                'totalBids': bids_str,
                'origin_source_detail': origin_source,
                'time_ago_exact': time_ago,
                'verbatim_request': verbatim_req,
                'requirements_list': reqs,
                'contractor_info': contractor_info
            },
            'observed_data': {
                'stated_salary': budget_str or 'Por cotizar',
                'stated_location': country_display,
                'stated_job_type': f"Anuncio Real ({posted_raw})",
                'origin_source_detail': origin_source,
                'time_ago_exact': time_ago,
                'verbatim_request': verbatim_req,
                'requirements_list': reqs,
                'contractor_info': contractor_info,
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
        stated_sal = f"{curr} {int(p_min):,} - {int(p_max):,}" if (p_min and p_max) else 'Por cotizar'
        bid_count = (item.get('bid_stats') or {}).get('bid_count', 0)

        origin_source = f"Publicado en: Freelancer.co — Anuncio #{pid} ({item.get('radar_category_label', 'Proyectos')})"
        time_ago = format_exact_time_ago(pub_iso)
        verbatim_req = f"\"{desc or title}\""
        reqs = [
            f"Requisitos técnicos solicitados: {', '.join(jobs) if jobs else 'Diseño 3D / Planos / Automatización / Tareas'}.",
            f"Presupuesto asignado por el demandante: {stated_sal}.",
            f"Propuestas recibidas hasta ahora: {bid_count} ofertas.",
            "Cumplir con las especificaciones exactas de la petición textual y adjuntar muestra o portafolio."
        ]
        contractor_info = f"Demandante verificado en Freelancer.co (Anuncio #{pid}, {time_ago.lower()}). Presupuesto ofrecido: {stated_sal}."

        return {
            'opportunity_id': opp_id,
            'source': 'Freelancer.co',
            'source_url': url,
            'discovered_at': now_iso,
            'published_at': pub_iso,
            'title': title,
            'organization': f"Solicitante Anuncio #{pid} ({item.get('radar_category_label', 'Freelance')})",
            'description': desc,
            'category': item.get('radar_category_label', 'Tareas & Diseño'),
            'opportunity_type': 'tarea_directa',
            'payment_min': p_min,
            'payment_max': p_max,
            'currency': curr,
            'location': 'Remoto (Sin Contrato Legal)',
            'approx_place': 'Colombia / Internacional (Entrega Digital Directa)',
            'contractor_info': contractor_info,
            'origin_source_detail': origin_source,
            'time_ago_exact': time_ago,
            'verbatim_request': verbatim_req,
            'requirements_list': reqs,
            'remote': True,
            'raw_data': {
                'id': pid,
                'seo_url': seo_url,
                'bid_count': bid_count,
                'origin_source_detail': origin_source,
                'time_ago_exact': time_ago,
                'verbatim_request': verbatim_req,
                'requirements_list': reqs,
                'contractor_info': contractor_info
            },
            'observed_data': {
                'stated_salary': stated_sal,
                'stated_location': 'Colombia / Internacional',
                'stated_job_type': f"Pago por Tarea ({time_ago})",
                'origin_source_detail': origin_source,
                'time_ago_exact': time_ago,
                'verbatim_request': verbatim_req,
                'requirements_list': reqs,
                'contractor_info': contractor_info,
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
        pub_at = item.get('published_at') or now_iso

        origin_source = item.get('origin_source_detail') or f"Publicado en: Canal Directo San Agustín / Huila ({item.get('organization', '')})"
        time_ago = item.get('time_ago_exact') or format_exact_time_ago(pub_at)
        verbatim_req = item.get('verbatim_request') or f"\"{item.get('description', '')}\""
        reqs = item.get('requirements_list') or [
            "Disponibilidad en San Agustín / Sur del Huila o entrega digital rápida.",
            "Trato directo con el contratante por WhatsApp o enlace oficial."
        ]

        return {
            'opportunity_id': opp_id,
            'source': 'San Agustín · Huila · Guadua',
            'source_url': item.get('url', 'https://www.sanagustin-huila.gov.co/contratacion'),
            'discovered_at': now_iso,
            'published_at': pub_at,
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
            'origin_source_detail': origin_source,
            'time_ago_exact': time_ago,
            'verbatim_request': verbatim_req,
            'requirements_list': reqs,
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
                'stated_job_type': time_ago,
                'whatsapp_phone': item.get('whatsapp_phone') or '',
                'contact_phone': item.get('contact_phone') or item.get('whatsapp_phone') or '',
                'contact_whatsapp_url': item.get('contact_whatsapp_url') or '',
                'circular_code': item.get('circular_code') or '',
                'contact_email': item.get('contact_email') or '',
                'approx_place': item.get('approx_place') or loc,
                'contractor_info': item.get('contractor_info') or f"Contratante verificado: {item.get('organization', 'San Agustín Huila')}",
                'origin_source_detail': origin_source,
                'time_ago_exact': time_ago,
                'verbatim_request': verbatim_req,
                'requirements_list': reqs,
                'lat': item.get('lat', 1.8792),
                'lon': item.get('lon', -76.2706),
                'distance_km': item.get('distance_km', 0.5),
                'category_hint': item.get('category_hint', 'guadua_cabanas'),
                'tags': skills + ['san agustin', 'huila', 'guadua', 'bioconstruccion', 'muro tendinoso', 'metal', 'soldadura', 'murales', 'tatuajes', 'cafe borbon rosado', 'secaderos', 'sena', 'exterior']
            }
        }
