from http.server import BaseHTTPRequestHandler
import json
import os

# Default events data
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
    """Get events from Vercel KV or fallback to default."""
    try:
        from vercel_kv import KV
        kv = KV()
        data = kv.get('events_data')
        if data:
            return json.loads(data) if isinstance(data, str) else data
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
