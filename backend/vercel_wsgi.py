import os
import sys
import json

# Configure paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
os.environ["VERCEL"] = "1"
os.environ["DEBUG"] = "True"
os.environ["ALLOWED_HOSTS"] = "*"

# Create a minimal application
def application(environ, start_response):
    # Basic health check response
    status = '200 OK'
    headers = [
        ('Content-type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),
        ('Access-Control-Allow-Headers', '*')
    ]
    start_response(status, headers)
    response = {'status': 'ok', 'message': 'API is responding'}
    return [json.dumps(response).encode()]

# Simple handler for Vercel
def handler(event, context):
    # Basic response for direct invocation
    if 'path' in event and event['path'].endswith('/api/health'):
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': '*'
            },
            'body': json.dumps({
                'status': 'ok',
                'message': 'Simple health check responding',
                'environment': 'Vercel',
                'path': event.get('path', 'unknown')
            })
        }
    
    # Preflight response for OPTIONS requests
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 204,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }
    
    # For other paths, return a 501 Not Implemented for now
    return {
        'statusCode': 501,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        },
        'body': json.dumps({
            'status': 'error',
            'message': 'This endpoint is not implemented in the simplified handler',
            'path': event.get('path', 'unknown')
        })
    } 