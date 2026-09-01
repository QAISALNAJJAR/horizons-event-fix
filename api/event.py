from http.server import BaseHTTPRequestHandler
import json
import os

def get_events_data():
    events_file = os.path.join(os.path.dirname(__file__), '..', 'events.json')
    try:
        with open(events_file, 'r') as f:
            return json.load(f)
    except:
        return {'events': [], 'activeEventId': None}

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
