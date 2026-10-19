import re
import html
import hashlib
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

def clean_html(raw_html):
    if not raw_html:
        return ''
    text = re.sub(r'<[^>]+>', ' ', str(raw_html))
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_date_iso(raw_date):
    """Converts Unix timestamps, RFC-2822, or ISO strings into canonical UTC ISO-8601 string."""
    if not raw_date:
        return datetime.now(timezone.utc).isoformat()
    try:
        if isinstance(raw_date, (int, float)) or (isinstance(raw_date, str) and raw_date.isdigit()):
            ts = float(raw_date)
            if ts > 1e12:
                ts /= 1000.0
            return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
        s = str(raw_date).strip()
        # Try RFC 2822 (e.g. "Tue, 15 Sep 2026 14:12:47 +0000")
        if ',' in s or 'GMT' in s or '+' in s and s[0].isalpha():
            dt = parsedate_to_datetime(s)
            return dt.astimezone(timezone.utc).isoformat()
        # Try ISO-8601
        s_iso = s.replace('Z', '+00:00')
        dt = datetime.fromisoformat(s_iso)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except Exception:
        return datetime.now(timezone.utc).isoformat()

def parse_salary_string(salary_str, require_currency=False):
    """
    Parses a salary string into (min, max, currency).
    If require_currency=True (used when scanning unstructured body text),
    only matches numbers explicitly attached to $, USD, EUR, €, £, GBP.
    """
    if not salary_str:
        return None, None, None

    s = str(salary_str).strip()
    if not s or s.lower() in ['competitive', 'undisclosed', 'negotiable', 'n/a', 'no publicado']:
        return None, None, None

    if require_currency:
        # Strict match: must have $, USD, EUR, €, £ right before or after the number
        pattern = r'(?:(\$|USD|EUR|€|£|GBP)\s*(\d[\d,]*(?:\.\d+)?)\s*(k|K)?|(\d[\d,]*(?:\.\d+)?)\s*(k|K)?\s*(USD|EUR|GBP|\$|€|£)\b)'
        matches = re.findall(pattern, s, re.IGNORECASE)
        if not matches:
            return None, None, None
        parsed_nums = []
        currency = 'USD'
        for m in matches:
            curr1, num1, k1, num2, k2, curr2 = m
            c_raw = (curr1 or curr2 or '$').upper()
            if c_raw in ['$', 'USD']:
                currency = 'USD'
            elif c_raw in ['€', 'EUR']:
                currency = 'EUR'
            elif c_raw in ['£', 'GBP']:
                currency = 'GBP'
            num_str = num1 or num2
            k_mult = k1 or k2
            try:
                val = float(num_str.replace(',', ''))
                if k_mult:
                    val *= 1000.0
                # Filter out obvious non-payment numbers like $0 or > $500,000
                if 15 <= val <= 450000:
                    parsed_nums.append(val)
            except ValueError:
                pass
        if not parsed_nums:
            return None, None, None
        if len(parsed_nums) == 1:
            return parsed_nums[0], parsed_nums[0], currency
        return min(parsed_nums[:2]), max(parsed_nums[:2]), currency

    currency = None
    if '$' in s or 'USD' in s.upper():
        currency = 'USD'
    elif '€' in s or 'EUR' in s.upper():
        currency = 'EUR'
    elif '£' in s or 'GBP' in s.upper():
        currency = 'GBP'

    if not currency:
        return None, None, None

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
            if 15 <= val <= 450000:
                parsed_nums.append(val)
        except ValueError:
            pass

    if not parsed_nums:
        return None, None, None
    if len(parsed_nums) == 1:
        return parsed_nums[0], parsed_nums[0], currency
    return min(parsed_nums), max(parsed_nums), currency

class OpportunityNormalizer:
    @staticmethod
    def normalize_remotive(item):
        now_iso = datetime.now(timezone.utc).isoformat()
        job_id = str(item.get('id', ''))
        url = item.get('url', '')
        opp_id = f'remotive_{job_id}' if job_id else f'remotive_{hashlib.md5(url.encode()).hexdigest()[:12]}'

        salary_str = item.get('salary', '')
        p_min, p_max, curr = parse_salary_string(salary_str, require_currency=False)
        clean_desc = clean_html(item.get('description', ''))

        job_type = (item.get('job_type') or '').lower()
        opp_type = 'contract' if ('contract' in job_type or 'freelance' in job_type) else ('full_time' if 'full' in job_type else 'general')
        pub_iso = normalize_date_iso(item.get('publication_date'))

        return {
            'opportunity_id': opp_id,
            'source': 'Remotive',
            'source_url': url,
            'discovered_at': now_iso,
            'published_at': pub_iso,
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
                'stated_salary': salary_str if (salary_str and p_min) else None,
                'stated_location': item.get('candidate_required_location') or 'Worldwide',
                'stated_job_type': item.get('job_type') or 'Remote',
                'tags': item.get('tags', [])
            }
        }

    @staticmethod
    def normalize_arbeitnow(item):
        now_iso = datetime.now(timezone.utc).isoformat()
        slug = item.get('slug', '')
        url = item.get('url', '')
        opp_id = f'arbeitnow_{slug}' if slug else f'arbeitnow_{hashlib.md5(url.encode()).hexdigest()[:12]}'

        clean_desc = clean_html(item.get('description', ''))
        job_types = [str(t).lower() for t in item.get('job_types', [])]
        opp_type = 'contract' if any('contract' in t or 'freelance' in t for t in job_types) else 'full_time'
        pub_iso = normalize_date_iso(item.get('created_at'))
        p_min, p_max, curr = parse_salary_string(clean_desc[:600], require_currency=True)

        return {
            'opportunity_id': opp_id,
            'source': 'Arbeitnow',
            'source_url': url,
            'discovered_at': now_iso,
            'published_at': pub_iso,
            'title': (item.get('title') or '').strip(),
            'organization': (item.get('company_name') or '').strip(),
            'description': clean_desc,
            'category': 'Software & Tech',
            'opportunity_type': opp_type,
            'payment_min': p_min,
            'payment_max': p_max,
            'currency': curr,
            'location': item.get('location') or 'Europe / Remote',
            'remote': bool(item.get('remote', False)),
            'raw_data': {
                'slug': item.get('slug'),
                'company_name': item.get('company_name'),
                'tags': item.get('tags', []),
                'job_types': item.get('job_types', [])
            },
            'observed_data': {
                'stated_salary': f"{curr} {int(p_min):,}" if (p_min and curr) else None,
                'stated_location': item.get('location') or 'Remote',
                'stated_job_type': ', '.join(item.get('job_types', [])) or 'Tech Role',
                'tags': item.get('tags', [])
            }
        }

    @staticmethod
    def normalize_remoteok(item):
        now_iso = datetime.now(timezone.utc).isoformat()
        job_id = str(item.get('id', ''))
        url = item.get('url', '')
        if not url and job_id:
            url = f"https://remoteok.com/remote-jobs/{job_id}"
        opp_id = f'remoteok_{job_id}' if job_id else f'remoteok_{hashlib.md5(url.encode()).hexdigest()[:12]}'

        clean_desc = clean_html(item.get('description', ''))

        p_min = None
        p_max = None
        try:
            if item.get('salary_min') and float(item['salary_min']) > 0:
                p_min = float(item['salary_min'])
            if item.get('salary_max') and float(item['salary_max']) > 0:
                p_max = float(item['salary_max'])
        except (ValueError, TypeError):
            pass

        stated_salary = None
        if p_min or p_max:
            stated_salary = f"USD {int(p_min or p_max):,}" + (f" - {int(p_max):,}" if (p_max and p_max != p_min) else "")

        tags = item.get('tags', [])
        is_contract = any(t.lower() in ['contract', 'freelance', 'hourly'] for t in tags)
        opp_type = 'contract' if is_contract else 'full_time'
        pub_iso = normalize_date_iso(item.get('date') or item.get('epoch'))

        return {
            'opportunity_id': opp_id,
            'source': 'RemoteOK',
            'source_url': url,
            'discovered_at': now_iso,
            'published_at': pub_iso,
            'title': (item.get('position') or '').strip(),
            'organization': (item.get('company') or '').strip(),
            'description': clean_desc,
            'category': 'Remote Tech',
            'opportunity_type': opp_type,
            'payment_min': p_min,
            'payment_max': p_max,
            'currency': 'USD' if (p_min or p_max) else None,
            'location': item.get('location') or 'Worldwide',
            'remote': True,
            'raw_data': {
                'id': item.get('id'),
                'company': item.get('company'),
                'tags': tags,
                'salary_min': item.get('salary_min'),
                'salary_max': item.get('salary_max')
            },
            'observed_data': {
                'stated_salary': stated_salary,
                'stated_location': item.get('location') or 'Worldwide',
                'stated_job_type': 'Contract' if is_contract else 'Full-time',
                'tags': tags
            }
        }

    @staticmethod
    def normalize_weworkremotely(item):
        now_iso = datetime.now(timezone.utc).isoformat()
        link = item.get('link', '')
        opp_id = f'wwr_{hashlib.md5(link.encode()).hexdigest()[:12]}'

        full_title = (item.get('title') or '').strip()
        parts = full_title.split(': ', 1)
        if len(parts) == 2:
            org, title = parts[0].strip(), parts[1].strip()
        else:
            org, title = 'WeWorkRemotely', full_title

        clean_desc = clean_html(item.get('description', ''))
        p_min, p_max, curr = parse_salary_string(clean_desc[:800], require_currency=True)
        pub_iso = normalize_date_iso(item.get('pubDate'))

        is_contract = bool(re.search(r'\b(contract|freelance|hourly|part-time)\b', f"{title} {clean_desc[:400]}", re.IGNORECASE))

        stated_sal = None
        if p_min and curr:
            stated_sal = f"{curr} {int(p_min):,}" + (f" - {int(p_max):,}" if (p_max and p_max != p_min) else "")

        return {
            'opportunity_id': opp_id,
            'source': 'WeWorkRemotely',
            'source_url': link,
            'discovered_at': now_iso,
            'published_at': pub_iso,
            'title': title,
            'organization': org,
            'description': clean_desc,
            'category': 'Remote Tech',
            'opportunity_type': 'contract' if is_contract else 'full_time',
            'payment_min': p_min,
            'payment_max': p_max,
            'currency': curr,
            'location': 'Worldwide',
            'remote': True,
            'raw_data': {
                'guid': item.get('guid'),
                'feed': item.get('feed_source')
            },
            'observed_data': {
                'stated_salary': stated_sal,
                'stated_location': 'Worldwide / Remote',
                'stated_job_type': 'Contract' if is_contract else 'Remote Role',
                'tags': []
            }
        }

    @staticmethod
    def normalize_hackernews(item):
        now_iso = datetime.now(timezone.utc).isoformat()
        object_id = str(item.get('objectID', ''))
        url = item.get('url') or f"https://news.ycombinator.com/item?id={object_id}"
        opp_id = f'hn_{object_id}' if object_id else f'hn_{hashlib.md5(url.encode()).hexdigest()[:12]}'

        author = item.get('author', 'HN Founder')
        raw_text = item.get('comment_text') or item.get('story_text') or item.get('title') or ''
        clean_desc = clean_html(raw_text)

        if item.get('title') and not item.get('comment_text'):
            title = item.get('title').strip()
            org = f"YC / {author}"
        else:
            first_chunk = clean_desc.split('.')[0].strip()
            if 10 < len(first_chunk) < 110:
                title = first_chunk
            else:
                title = f"Direct Founder Contract / Gig ({author})"
            org = f"HN: {author}"

        p_min, p_max, curr = parse_salary_string(clean_desc, require_currency=True)
        pub_iso = normalize_date_iso(item.get('created_at') or item.get('created_at_i'))

        stated_sal = None
        if p_min and curr:
            stated_sal = f"{curr} {int(p_min):,}" + (f" - {int(p_max):,}" if (p_max and p_max != p_min) else "")

        return {
            'opportunity_id': opp_id,
            'source': 'HackerNews',
            'source_url': f"https://news.ycombinator.com/item?id={object_id}" if object_id else url,
            'discovered_at': now_iso,
            'published_at': pub_iso,
            'title': title,
            'organization': org,
            'description': clean_desc,
            'category': 'Founder / Direct Contract',
            'opportunity_type': 'freelance',
            'payment_min': p_min,
            'payment_max': p_max,
            'currency': curr,
            'location': 'Remote / Worldwide',
            'remote': True,
            'raw_data': {
                'objectID': object_id,
                'author': author,
                'story_id': item.get('story_id')
            },
            'observed_data': {
                'stated_salary': stated_sal,
                'stated_location': 'Remote',
                'stated_job_type': 'Direct Freelance / Contract',
                'tags': ['hacker_news', 'direct_founder']
            }
        }

    @staticmethod
    def normalize_github_bounty(item):
        now_iso = datetime.now(timezone.utc).isoformat()
        issue_id = str(item.get('id', ''))
        url = item.get('html_url', '')
        opp_id = f'github_bounty_{issue_id}' if issue_id else f'github_bounty_{hashlib.md5(url.encode()).hexdigest()[:12]}'

        body = item.get('body', '') or ''
        clean_desc = clean_html(body)[:2500]

        full_text = f"{item.get('title', '')} {clean_desc}"
        p_min, p_max, curr = parse_salary_string(full_text, require_currency=True)

        org = 'GitHub Open Source'
        parts = url.replace('https://github.com/', '').split('/')
        if len(parts) >= 2:
            org = f'{parts[0]}/{parts[1]}'

        labels = [l.get('name', '') if isinstance(l, dict) else str(l) for l in item.get('labels', [])]
        pub_iso = normalize_date_iso(item.get('created_at'))

        return {
            'opportunity_id': opp_id,
            'source': 'GitHub Bounties',
            'source_url': url,
            'discovered_at': now_iso,
            'published_at': pub_iso,
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
                'stated_salary': f'{curr} {int(p_min):,}' if (p_min and curr) else 'Bounty Abierto',
                'stated_location': 'Worldwide / Remote',
                'stated_job_type': 'Bounty Issue',
                'tags': labels
            }
        }
