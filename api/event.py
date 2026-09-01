from http.server import BaseHTTPRequestHandler
import json
import urllib.request

# JSONBin.io free API
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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data = get_events_data()
        
        active_event = None
        for event in data.get('events', []):
            if event['id'] == data.get('activeEventId'):
                active_event = event
                break
        
        response = json.dumps({
            'activeEvent': active_event,
            'allEvents': data.get('events', [])
        })
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
