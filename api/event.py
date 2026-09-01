import json
import os
from http.server import BaseHTTPRequestHandler

# Read events from JSON file
def get_events_data():
    events_file = os.path.join(os.path.dirname(__file__), '..', 'events.json')
    try:
        with open(events_file, 'r') as f:
            return json.load(f)
    except:
        return {'events': [], 'activeEventId': None}

def app(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json'
    }
    
    if request.method == 'OPTIONS':
        return ('', 200, headers)
    
    data = get_events_data()
    
    if request.method == 'GET':
        active_event = None
        for event in data.get('events', []):
            if event['id'] == data.get('activeEventId'):
                active_event = event
                break
        
        return (json.dumps({
            'activeEvent': active_event,
            'allEvents': data.get('events', [])
        }), 200, headers)
    
    return (json.dumps({'error': 'Method not allowed'}), 405, headers)
