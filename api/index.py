from app import app

# Vercel expects a callable WSGI entrypoint.
# The root Flask application is exposed here so the deployment can serve it.
application = app
handler = app
