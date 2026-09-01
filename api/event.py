from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import json

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

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        active_event = None
        for event in DEFAULT_EVENTS.get('events', []):
            if event['id'] == DEFAULT_EVENTS.get('activeEventId'):
                active_event = event
                break
        
        response = json.dumps({
            'activeEvent': active_event,
            'allEvents': DEFAULT_EVENTS.get('events', [])
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
