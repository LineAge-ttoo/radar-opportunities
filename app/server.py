import sys
import os
import json
import time
import subprocess
import threading
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from scripts.utilities.db import get_all_opportunities, update_opportunity_status, get_stats
from scripts.utilities.whatsapp_auto_sender import auto_dispatch_to_whatsapp_3222739034

PORT = int(os.environ.get('PORT', 8080))
APP_DIR = os.path.join(BASE_DIR, 'app')
HTML_FILE = os.path.join(APP_DIR, 'index.html')
MANIFEST_FILE = os.path.join(APP_DIR, 'manifest.json')
SNAPSHOT_FILE = os.path.join(APP_DIR, 'latest_scan.json')

is_scanning = False
last_scan_result = None


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def periodic_auto_scan_and_whatsapp():
    """Hilo automático en segundo plano: actualiza varias veces al día y despacha alertas a +57 3222739034."""
    global is_scanning, last_scan_result
    while True:
        time.sleep(2 * 3600)  # Cada 2 horas
        if not is_scanning:
            is_scanning = True
            try:
                scan_script = os.path.join(BASE_DIR, 'scripts', 'run_radar_scan.py')
                res = subprocess.run([sys.executable, scan_script], capture_output=True, text=True, cwd=BASE_DIR)
                last_scan_result = {'success': res.returncode == 0}
            except Exception:
                pass
            finally:
                is_scanning = False


class RadarHttpHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path in ['/', '/index.html', '/app', '/app/index.html']:
            if os.path.exists(HTML_FILE):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                with open(HTML_FILE, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "index.html not found")

        elif path in ['/manifest.json', '/app/manifest.json']:
            if os.path.exists(MANIFEST_FILE):
                self.send_response(200)
                self.send_header('Content-Type', 'application/manifest+json; charset=utf-8')
                self.end_headers()
                with open(MANIFEST_FILE, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "manifest.json not found")

        elif path in ['/latest_scan.json', '/app/latest_scan.json', '/data/opportunities/latest_scan.json']:
            if os.path.exists(SNAPSHOT_FILE):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Cache-Control', 'no-cache')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                with open(SNAPSHOT_FILE, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "latest_scan.json not found")

        elif path == '/api/stats':
            stats = get_stats()
            stats['local_ip'] = get_local_ip()
            stats['port'] = PORT
            stats['is_scanning'] = is_scanning
            self.send_json(stats)

        elif path == '/api/opportunities':
            decision = query.get('decision', [None])[0]
            status = query.get('status', [None])[0]
            search = query.get('search', [None])[0]
            limit = int(query.get('limit', [250])[0])

            opps = get_all_opportunities(filter_decision=decision, filter_status=status, limit=limit)
            if search:
                s_lower = search.lower()
                opps = [
                    o for o in opps
                    if s_lower in o.get('title', '').lower()
                    or s_lower in o.get('organization', '').lower()
                    or any(s_lower in s.lower() for s in o.get('skills', []))
                    or s_lower in o.get('description', '').lower()
                ]

            self.send_json({'count': len(opps), 'opportunities': opps})

        elif path == '/api/scan/status':
            self.send_json({'is_scanning': is_scanning, 'last_scan': last_scan_result})

        else:
            self.send_error(404, "Endpoint not found")

    def do_POST(self):
        global is_scanning, last_scan_result
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get('Content-Length', 0))
        raw_b = self.rfile.read(content_length) if content_length > 0 else b'{}'
        try:
            body = raw_b.decode('utf-8')
        except Exception:
            body = raw_b.decode('cp1252', errors='replace')
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if path == '/api/scan':
            if is_scanning:
                self.send_json({'error': 'Scan already in progress', 'is_scanning': True}, status_code=409)
                return

            def background_scan():
                global is_scanning, last_scan_result
                is_scanning = True
                try:
                    scan_script = os.path.join(BASE_DIR, 'scripts', 'run_radar_scan.py')
                    res = subprocess.run([sys.executable, scan_script], capture_output=True, text=True, cwd=BASE_DIR)
                    last_scan_result = {
                        'success': res.returncode == 0,
                        'stdout': res.stdout[-800:] if res.stdout else '',
                        'stderr': res.stderr[-400:] if res.stderr else ''
                    }
                except Exception as e:
                    last_scan_result = {'success': False, 'error': str(e)}
                finally:
                    is_scanning = False

            t = threading.Thread(target=background_scan, daemon=True)
            t.start()
            self.send_json({'message': 'Scan triggered successfully', 'is_scanning': True})

        elif path == '/api/auto-whatsapp':
            opps = get_all_opportunities(limit=60)
            result = auto_dispatch_to_whatsapp_3222739034(opps, force=bool(payload.get('force', False)))
            self.send_json(result)

        elif path == '/api/opportunity/status':
            opp_id = payload.get('opportunity_id')
            new_status = payload.get('status')
            notes = payload.get('notes')
            if not opp_id or not new_status:
                self.send_json({'error': 'Missing opportunity_id or status'}, status_code=400)
                return
            update_opportunity_status(opp_id, new_status, notes=notes)
            self.send_json({'success': True, 'opportunity_id': opp_id, 'new_status': new_status})

        else:
            self.send_error(404, "Endpoint not found")


def run_server():
    t = threading.Thread(target=periodic_auto_scan_and_whatsapp, daemon=True)
    t.start()
    server_address = ('0.0.0.0', PORT)
    httpd = HTTPServer(server_address, RadarHttpHandler)
    local_ip = get_local_ip()
    print("="*58)
    print(" QUE HAY PA HACER! - CYBER-ZEN SERVER (SAN AGUSTIN HUILA)")
    print("="*58)
    print(f"PC Local:        http://127.0.0.1:{PORT}")
    print(f"Safari / Movil:  http://{local_ip}:{PORT}")
    print("="*58)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
