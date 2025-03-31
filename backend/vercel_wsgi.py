import os
import sys
import json
import traceback

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
os.environ["VERCEL"] = "1"
os.environ["DEBUG"] = "False"
os.environ["ALLOWED_HOSTS"] = "*"

# Import Django only after setting environment variables
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("Django application initialized successfully")
except Exception as e:
    print(f"ERROR initializing Django application: {str(e)}")
    traceback.print_exc()
    # Don't re-raise, allow handler to respond with error details

# Create a simple endpoint for health checks
def handler(request, **kwargs):
    """Vercel serverless handler"""
    
    # Get request method and path
    method = request.get("method", "").upper()
    path = request.get("path", "").strip("/")
    
    # Debug information
    print(f"Request received: {method} /{path}")
    print(f"Request body: {request.get('body', '')}")
    print(f"Headers: {json.dumps(request.get('headers', {}))}")
    
    # Handle all OPTIONS requests directly without going to Django
    if method == "OPTIONS":
        print(f"Handling OPTIONS request for /{path}")
        return {
            "statusCode": 204,
            "headers": {
                "Access-Control-Allow-Origin": "https://frrontend.vercel.app",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Max-Age": "86400"
            },
            "body": ""
        }
    
    # Direct health check response
    if path == "api/health" or path == "health":
        print("Serving health check response")
        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "ok",
                "message": "API is responding (direct handler)",
                "environment": "Vercel"
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        }
    
    # For all other requests, try to use Django but with error handling
    try:
        print(f"Delegating to Django application: {path}")
        resp = application(request, **kwargs)
        print(f"Django response: {resp}")
        return resp
    except Exception as e:
        print(f"ERROR in handler: {str(e)}")
        traceback.print_exc()
        
        # Return error as JSON
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Server Error",
                "message": str(e),
                "path": path,
                "traceback": traceback.format_exc()
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*"
            }
        } 