import json
import os

# Simple password protection
API_PASSWORD = 'horizons2026'

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
    
    # Check authorization
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header[7:] != API_PASSWORD:
        return (json.dumps({'error': 'Unauthorized'}), 401, headers)
    
    # Read events from JSON file
    events_file = os.path.join(os.path.dirname(__file__), '..', 'events.json')
    try:
        with open(events_file, 'r') as f:
            data = json.load(f)
    except:
        data = {'events': [], 'activeEventId': None}
    
    if request.method == 'GET':
        return (json.dumps(data), 200, headers)
    
    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            action = body.get('action')
            
            if action == 'add':
                event_id = body.get('id')
                title = body.get('title', 'Untitled')
                if not event_id:
                    return (json.dumps({'error': 'Missing event id'}), 400, headers)
                
                # Remove if exists
                data['events'] = [e for e in data['events'] if e['id'] != event_id]
                data['events'].append({'id': event_id, 'title': title})
                
                # Set as active if first event
                if not data.get('activeEventId'):
                    data['activeEventId'] = event_id
                    
            elif action == 'remove':
                event_id = body.get('id')
                data['events'] = [e for e in data['events'] if e['id'] != event_id]
                if data.get('activeEventId') == event_id:
                    data['activeEventId'] = data['events'][0]['id'] if data['events'] else None
                    
            elif action == 'setActive':
                event_id = body.get('id')
                if any(e['id'] == event_id for e in data['events']):
                    data['activeEventId'] = event_id
                else:
                    return (json.dumps({'error': 'Event not found'}), 404, headers)
            
            # Save to file
            with open(events_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return (json.dumps({'success': True, 'data': data}), 200, headers)
        except Exception as e:
            return (json.dumps({'error': str(e)}), 400, headers)
    
    return (json.dumps({'error': 'Method not allowed'}), 405, headers)
