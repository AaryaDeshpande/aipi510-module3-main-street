"""WSGI entry point for Flask-aware Python hosts such as Vercel."""
from business_app.web import create_app

app = create_app()
