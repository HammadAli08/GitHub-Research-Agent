import sys
import os

# Add the parent directory to sys.path so we can import from the root and 'backend'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app as fastapi_app

# This is required for Vercel to correctly route requests to the FastAPI app
# when using /api/(.*) rewrites
class StripApiPrefix:
    def __init__(self, app):
        self.app = app
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            if path.startswith("/api"):
                # Strip /api from the beginning of the path
                scope["path"] = path[4:]
                if not scope["path"]:
                    scope["path"] = "/"
        await self.app(scope, receive, send)

# Export the wrapped app as 'app' for Vercel
app = StripApiPrefix(fastapi_app)
