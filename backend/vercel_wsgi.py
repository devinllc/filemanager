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
    
    # Simplify path handling to avoid double /api/api
    path = request.get("path", "").strip("/")
    if path == "api/health" or path == "health":
        # Direct health check response
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
    
    # Handle OPTIONS requests for CORS preflight
    if request.get("method") == "OPTIONS":
        return {
            "statusCode": 204,
            "headers": {
                "Access-Control-Allow-Origin": "https://frrontend.vercel.app",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Max-Age": "86400"
            }
        }
    
    # For all other Django requests
    try:
        return application(request, **kwargs)
    except Exception as e:
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