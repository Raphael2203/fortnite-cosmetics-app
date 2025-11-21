from app.api.main import app as _app

# Expose 'app' at this module level so uvicorn/reloaders expecting "app.main:app" work.
app = _app

# Optional friendly name for tools
__all__ = ["app"]
