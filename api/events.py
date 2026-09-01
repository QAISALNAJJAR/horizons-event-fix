from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error

API_PASSWORD = 'horizons2026'

# JSONBin.io free API - sign up at https://jsonbin.io to get your bin ID
# This is a free JSON storage service
JSONBIN_ID = '6a96ed54f5f4af5e295d224b'
JSONBIN_API_KEY = '$2a$10$f/iO1sJfQqWXCMn1A494BuUH.qTmIzEyc6EesZB2wnLcmXXffXBUy'
JSONBIN_URL = f'https://api.jsonbin.io/v3/b/{JSONBIN_ID}'

DEFAULT_EVENTS = {
    "events": [
        {
            "id": "3b68b316-6f6d-4a40-ae99-1476da708be8",
            "title": "UWC Boarding School Info Session"
        }
    ],
    "activeEventId": "3b68b316-6f6d-4a40-ae99-1476da708be8"
}

def get_events_data():
    """Get events from JSONBin.io or fallback to default."""
    try:
        req = urllib.request.Request(
            f'{JSONBIN_URL}/latest',
            headers={
                'X-Access-Key': JSONBIN_API_KEY,
                'X-Bin-Meta': 'false'
            }
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return data.get('record', data)
    except:
        pass
    return DEFAULT_EVENTS.copy()

def save_events_data(data):
    """Save events to JSONBin.io."""
    try:
        req = urllib.request.Request(
            JSONBIN_URL,
            data=json.dumps(data).encode(),
            method='PUT',
            headers={
                'Content-Type': 'application/json',
                'X-Access-Key': JSONBIN_API_KEY
            }
        )
        urllib.request.urlopen(req, timeout=5)
    except:
        pass

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
        self.wfile.write(json.dumps(get_events_data()).encode())
    
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
            events_data = get_events_data()
            
            if action == 'add':
                event_id = data.get('id')
                title = data.get('title', 'Untitled')
                if not event_id:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Missing event id'}).encode())
                    return
                
                events_data['events'] = [e for e in events_data['events'] if e['id'] != event_id]
                events_data['events'].append({'id': event_id, 'title': title})
                
                if not events_data.get('activeEventId'):
                    events_data['activeEventId'] = event_id
                    
            elif action == 'remove':
                event_id = data.get('id')
                events_data['events'] = [e for e in events_data['events'] if e['id'] != event_id]
                if events_data.get('activeEventId') == event_id:
                    events_data['activeEventId'] = events_data['events'][0]['id'] if events_data['events'] else None
                    
            elif action == 'setActive':
                event_id = data.get('id')
                if any(e['id'] == event_id for e in events_data['events']):
                    events_data['activeEventId'] = event_id
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Event not found'}).encode())
                    return
            
            save_events_data(events_data)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'data': events_data}).encode())
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
