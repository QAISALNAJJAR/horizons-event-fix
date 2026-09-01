import json
import os

def handler(request):
    # Enable CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json'
    }
    
    if request.method == 'OPTIONS':
        return ('', 200, headers)
    
    # Read events from JSON file
    events_file = os.path.join(os.path.dirname(__file__), '..', 'events.json')
    try:
        with open(events_file, 'r') as f:
            data = json.load(f)
    except:
        data = {'events': [], 'activeEventId': None}
    
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
