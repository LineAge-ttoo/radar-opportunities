import urllib.request
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

class WeWorkRemotelyCollector:
    NAME = 'WeWorkRemotely'
    FEEDS = [
        'https://weworkremotely.com/categories/remote-programming-jobs.rss',
        'https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss',
        'https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss',
        'https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss'
    ]

    def __init__(self, timeout=25):
        self.timeout = timeout

    def collect(self, limit_per_feed=20):
        all_items = []
        seen_links = set()
        errors = []

        for feed_url in self.FEEDS:
            req = urllib.request.Request(
                feed_url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) RADAR/2.0'}
            )
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    xml_data = response.read().decode('utf-8')
                    root = ET.fromstring(xml_data)
                    channel = root.find('channel')
                    if channel is not None:
                        items = channel.findall('item')[:limit_per_feed]
                        for it in items:
                            title = it.find('title').text if it.find('title') is not None else ''
                            link = it.find('link').text if it.find('link') is not None else ''
                            if link in seen_links:
                                continue
                            seen_links.add(link)
                            desc = it.find('description').text if it.find('description') is not None else ''
                            pub_date = it.find('pubDate').text if it.find('pubDate') is not None else ''
                            guid = it.find('guid').text if it.find('guid') is not None else link

                            all_items.append({
                                'guid': guid,
                                'title': title,
                                'link': link,
                                'description': desc,
                                'pubDate': pub_date,
                                'feed_source': feed_url
                            })
            except Exception as e:
                errors.append(f"{feed_url}: {str(e)}")

        try:
            incoming_dir = os.path.join(BASE_DIR, 'data', 'incoming')
            os.makedirs(incoming_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            dump_path = os.path.join(incoming_dir, f'wwr_{timestamp}.json')
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
