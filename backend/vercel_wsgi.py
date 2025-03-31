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
    
    # Special case for health checks to avoid Django for simple checks
    if request.get("path", "").strip("/") == "api/health":
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
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            }
        }
    
    # Handle OPTIONS requests for CORS preflight
    if request.get("method") == "OPTIONS":
        return {
            "statusCode": 204,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization",
                "Access-Control-Max-Age": "86400"
            }
        }
    
    try:
        # For all other routes, use Django
        return application(request, **kwargs)
    except Exception as e:
        # Return error as JSON
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Server Error",
                "message": str(e)
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        } 