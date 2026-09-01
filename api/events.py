from http.server import BaseHTTPRequestHandler
import json

API_PASSWORD = 'horizons2026'

DEFAULT_EVENTS = {
    "events": [
        {
            "id": "3b68b316-6f6d-4a40-ae99-1476da708be8",
            "title": "UWC Boarding School Info Session"
        }
    ],
    "activeEventId": "3b68b316-6f6d-4a40-ae99-1476da708be8"
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        auth = self.headers.get('Authorization', '')
        if not auth.startswith('Bearer ') or auth[7:] != API_PASSWORD:
            self.send_response(401)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode())
            return
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(DEFAULT_EVENTS).encode())
    
    def do_POST(self):
        auth = self.headers.get('Authorization', '')
        if not auth.startswith('Bearer ') or auth[7:] != API_PASSWORD:
            self.send_response(401)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode())
            return
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body)
            action = data.get('action')
            
            if action == 'add':
                event_id = data.get('id')
                title = data.get('title', 'Untitled')
                DEFAULT_EVENTS['events'] = [e for e in DEFAULT_EVENTS['events'] if e['id'] != event_id]
                DEFAULT_EVENTS['events'].append({'id': event_id, 'title': title})
                if not DEFAULT_EVENTS.get('activeEventId'):
                    DEFAULT_EVENTS['activeEventId'] = event_id
                    
            elif action == 'remove':
                event_id = data.get('id')
                DEFAULT_EVENTS['events'] = [e for e in DEFAULT_EVENTS['events'] if e['id'] != event_id]
                if DEFAULT_EVENTS.get('activeEventId') == event_id:
                    DEFAULT_EVENTS['activeEventId'] = DEFAULT_EVENTS['events'][0]['id'] if DEFAULT_EVENTS['events'] else None
                    
            elif action == 'setActive':
                event_id = data.get('id')
                if any(e['id'] == event_id for e in DEFAULT_EVENTS['events']):
                    DEFAULT_EVENTS['activeEventId'] = event_id
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'data': DEFAULT_EVENTS}).encode())
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
