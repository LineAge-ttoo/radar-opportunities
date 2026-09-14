import re
import html
import hashlib
from datetime import datetime

def clean_html(raw_html):
    if not raw_html:
        return ''
    text = re.sub(r'<[^>]+>', ' ', str(raw_html))
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_salary_string(salary_str):
    if not salary_str:
        return None, None, None
    
    s = str(salary_str).strip()
    if not s or s.lower() in ['competitive', 'undisclosed', 'negotiable', 'n/a', 'no publicado']:
        return None, None, None

    currency = None
    if '$' in s or 'USD' in s:
        currency = 'USD'
    elif '€' in s or 'EUR' in s:
        currency = 'EUR'
    elif '£' in s or 'GBP' in s:
        currency = 'GBP'

    matches = re.findall(r'(\d+[\d,]*(?:\.\d+)?)\s*(k|K)?', s)
    parsed_nums = []
    for num_str, k_mult in matches:
        clean_num = num_str.replace(',', '')
        try:
            val = float(clean_num)
            if k_mult:
                val *= 1000
            elif val < 1000 and ('yr' in s.lower() or 'year' in s.lower() or 'annual' in s.lower()):
                val *= 1000
            parsed_nums.append(val)
        except ValueError:
            pass

    if not parsed_nums:
        return None, None, currency
    if len(parsed_nums) == 1:
        return parsed_nums[0], parsed_nums[0], currency
    return min(parsed_nums), max(parsed_nums), currency

class OpportunityNormalizer:
    @staticmethod
    def normalize_remotive(item):
        now_iso = datetime.now().isoformat()
        job_id = str(item.get('id', ''))
        url = item.get('url', '')
        if job_id:
            opp_id = f'remotive_{job_id}'
        else:
            opp_id = 'remotive_' + hashlib.md5(url.encode()).hexdigest()[:12]
        
        salary_str = item.get('salary', '')
        p_min, p_max, curr = parse_salary_string(salary_str)
        clean_desc = clean_html(item.get('description', ''))
        
        job_type = (item.get('job_type') or '').lower()
        opp_type = 'contract' if 'contract' in job_type or 'freelance' in job_type else ('full_time' if 'full' in job_type else 'general')

        return {
            'opportunity_id': opp_id,
            'source': 'Remotive',
            'source_url': url,
            'discovered_at': now_iso,
            'published_at': item.get('publication_date'),
            'title': (item.get('title') or '').strip(),
            'organization': (item.get('company_name') or '').strip(),
            'description': clean_desc,
            'category': (item.get('category') or 'Software Development').strip(),
            'opportunity_type': opp_type,
            'payment_min': p_min,
            'payment_max': p_max,
            'currency': curr,
            'location': item.get('candidate_required_location') or 'Worldwide',
            'remote': True,
            'raw_data': {
                'id': item.get('id'),
                'company_name': item.get('company_name'),
                'salary_raw': salary_str,
                'candidate_required_location': item.get('candidate_required_location'),
                'tags': item.get('tags', [])
            },
            'observed_data': {
                'stated_salary': salary_str if salary_str else None,
                'stated_location': item.get('candidate_required_location'),
                'stated_job_type': item.get('job_type'),
                'tags': item.get('tags', [])
            }
        }

    @staticmethod
    def normalize_arbeitnow(item):
        now_iso = datetime.now().isoformat()
        slug = item.get('slug', '')
        url = item.get('url', '')
        if slug:
            opp_id = f'arbeitnow_{slug}'
        else:
            opp_id = 'arbeitnow_' + hashlib.md5(url.encode()).hexdigest()[:12]
        
        clean_desc = clean_html(item.get('description', ''))
        job_types = [str(t).lower() for t in item.get('job_types', [])]
        opp_type = 'contract' if any('contract' in t or 'freelance' in t for t in job_types) else 'full_time'

        return {
            'opportunity_id': opp_id,
            'source': 'Arbeitnow',
            'source_url': url,
            'discovered_at': now_iso,
            'published_at': item.get('created_at'),
            'title': (item.get('title') or '').strip(),
            'organization': (item.get('company_name') or '').strip(),
            'description': clean_desc,
            'category': 'Software & Tech',
            'opportunity_type': opp_type,
            'payment_min': None,
            'payment_max': None,
            'currency': None,
            'location': item.get('location') or 'Worldwide',
            'remote': bool(item.get('remote', False)),
            'raw_data': {
                'slug': item.get('slug'),
                'company_name': item.get('company_name'),
                'tags': item.get('tags', []),
                'job_types': item.get('job_types', [])
            },
            'observed_data': {
                'stated_salary': None,
                'stated_location': item.get('location'),
                'stated_job_type': ', '.join(item.get('job_types', [])),
                'tags': item.get('tags', [])
            }
        }

    @staticmethod
    def normalize_github_bounty(item):
        now_iso = datetime.now().isoformat()
        issue_id = str(item.get('id', ''))
        url = item.get('html_url', '')
        if issue_id:
            opp_id = f'github_bounty_{issue_id}'
        else:
            opp_id = 'github_bounty_' + hashlib.md5(url.encode()).hexdigest()[:12]
        
        body = item.get('body', '') or ''
        clean_desc = clean_html(body)[:2000]

        full_text = f"{item.get('title', '')} {clean_desc}"
        p_min, p_max, curr = parse_salary_string(full_text)

        org = 'GitHub Open Source'
        parts = url.replace('https://github.com/', '').split('/')
        if len(parts) >= 2:
            org = f'{parts[0]}/{parts[1]}'

        labels = [l.get('name', '') if isinstance(l, dict) else str(l) for l in item.get('labels', [])]

        return {
            'opportunity_id': opp_id,
            'source': 'GitHub Bounties',
            'source_url': url,
            'discovered_at': now_iso,
            'published_at': item.get('created_at'),
            'title': (item.get('title') or '').strip(),
            'organization': org,
            'description': clean_desc,
            'category': 'Open Source / Bounty',
            'opportunity_type': 'bounty',
            'payment_min': p_min,
            'payment_max': p_max,
            'currency': curr,
            'location': 'Worldwide',
            'remote': True,
            'raw_data': {
                'id': item.get('id'),
                'html_url': url,
                'labels': labels,
                'user': item.get('user', {}).get('login') if isinstance(item.get('user'), dict) else None
            },
            'observed_data': {
                'stated_salary': f'{curr} {p_min}' if p_min and curr else None,
                'stated_location': 'Worldwide / Remote',
                'stated_job_type': 'Bounty Issue',
                'tags': labels
            }
        }
