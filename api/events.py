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
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    # Check authorization
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer ') or auth_header[7:] != API_PASSWORD:
        return {
            'statusCode': 401,
            'headers': headers,
            'body': json.dumps({'error': 'Unauthorized'})
        }
    
    # Read events from JSON file
    events_file = os.path.join(os.path.dirname(__file__), '..', 'events.json')
    try:
        with open(events_file, 'r') as f:
            data = json.load(f)
    except:
        data = {'events': [], 'activeEventId': None}
    
    if request.method == 'GET':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(data)
        }
    
    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            action = body.get('action')
            
            if action == 'add':
                event_id = body.get('id')
                title = body.get('title', 'Untitled')
                if not event_id:
                    return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Missing event id'})}
                
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
                    return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Event not found'})}
            
            # Save to file
            with open(events_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'success': True, 'data': data})
            }
        except Exception as e:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': str(e)})
            }
    
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({'error': 'Method not allowed'})
    }
