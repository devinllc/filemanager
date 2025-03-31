import json

def handler(event, context):
    """
    A very simple handler for Vercel serverless functions
    """
    path = event.get('path', '')
    method = event.get('httpMethod', 'GET')
    
    print(f"Request received: {method} {path}")
    print(f"Headers: {json.dumps(event.get('headers', {}))}")
    
    # Set CORS headers for all responses
    headers = {
        'Access-Control-Allow-Origin': 'https://frrontend.vercel.app',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Max-Age': '86400',
        'Content-Type': 'application/json'
    }
    
    # Handle OPTIONS preflight requests
    if method == 'OPTIONS':
        return {
            'statusCode': 204,
            'headers': headers,
            'body': ''
        }
    
    # Health check endpoint
    if path.endswith('/api/health'):
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'status': 'ok',
                'message': 'API is up and running',
                'server_info': {
                    'time': 'static response',
                    'path': path,
                    'method': method
                }
            })
        }
    
    # Mock login endpoint
    if path.endswith('/login') or path.endswith('/login/'):
        if method == 'POST':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'status': 'success',
                    'token': 'mock_token_for_testing',
                    'user': {
                        'id': 1,
                        'username': 'testuser',
                        'email': 'test@example.com'
                    }
                })
            }
    
    # Default response for unhandled paths
    return {
        'statusCode': 404,
        'headers': headers,
        'body': json.dumps({
            'status': 'error',
            'message': 'Endpoint not found',
            'path': path
        })
    } 