import os
import sys
import json

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
os.environ["VERCEL"] = "1"
os.environ["DEBUG"] = "False"
os.environ["ALLOWED_HOSTS"] = "*"

# Import Django only after setting environment variables
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Create a simple endpoint for health checks
def handler(request, **kwargs):
    """Vercel serverless handler"""
    
    # Get request method and path
    method = request.get("method", "").upper()
    path = request.get("path", "").strip("/")
    
    # Debug information
    print(f"Request received: {method} /{path}")
    print(f"Headers: {request.get('headers', {})}")
    
    # Special handling for OPTIONS method (CORS preflight)
    if method == "OPTIONS":
        print(f"Handling OPTIONS request for /{path}")
        return {
            "statusCode": 204,
            "headers": {
                "Access-Control-Allow-Origin": "https://frrontend.vercel.app",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Max-Age": "86400"
            },
            "body": ""
        }
    
    # Direct health check response
    if path == "api/health":
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
                "Access-Control-Allow-Origin": "https://frrontend.vercel.app",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
                "Access-Control-Allow-Credentials": "true"
            }
        }
    
    # Special handling for login endpoint
    if path == "api/login" or path == "api/login/":
        if method == "POST":
            print("Handling login request")
            try:
                # Pass to Django application
                return application(request, **kwargs)
            except Exception as e:
                print(f"Error in login: {str(e)}")
                return {
                    "statusCode": 500,
                    "body": json.dumps({
                        "error": "Login Error",
                        "message": str(e)
                    }),
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "https://frrontend.vercel.app",
                        "Access-Control-Allow-Credentials": "true"
                    }
                }
    
    # For all other Django requests
    try:
        print(f"Delegating to Django application: {path}")
        return application(request, **kwargs)
    except Exception as e:
        print(f"Error in handler: {str(e)}")
        # Return error as JSON
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Server Error",
                "message": str(e),
                "path": path
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "https://frrontend.vercel.app",
                "Access-Control-Allow-Credentials": "true"
            }
        } 