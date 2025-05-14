from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    """Create and configure the Flask application."""
    load_dotenv()
    app = Flask(__name__)
    app.config['STARLING_API_BASE_URL'] = 'https://api-sandbox.starlingbank.com/api/v2'
    app.config['STARLING_AUTH_TOKEN'] = os.getenv('STARLING_AUTH_TOKEN')

    if not app.config['STARLING_AUTH_TOKEN']:
        raise RuntimeError("STARLING_AUTH_TOKEN is missing in environment.")

    from .views import main_bp
    app.register_blueprint(main_bp)

    return app