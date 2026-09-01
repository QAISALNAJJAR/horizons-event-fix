import json
import os

def app(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    # Read events from JSON file
    events_file = os.path.join(os.path.dirname(__file__), '..', 'events.json')
    try:
        with open(events_file, 'r') as f:
            data = json.load(f)
    except:
        data = {'events': [], 'activeEventId': None}
    
    active_event = None
    for event in data.get('events', []):
        if event['id'] == data.get('activeEventId'):
            active_event = event
            break
    
    body = json.dumps({
        'activeEvent': active_event,
        'allEvents': data.get('events', [])
    })
    
    return (body, 200, headers)
