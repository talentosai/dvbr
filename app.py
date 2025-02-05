from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect
from os import environ as env
from stytch import Client
from routes import register_routes


def create_app():
    app = Flask(__name__, static_folder='static')
    app.secret_key = env.get('app_secret')
    
    # Initialize Bootstrap
    bootstrap = Bootstrap5(app)
    
    # Initialize CSRF protection
    csrf = CSRFProtect(app)
    
    # Initialize Stytch client
    app.stytch_client = Client(
        project_id=env.get("STYTCH_PROJECT_ID"),
        secret=env.get("STYTCH_SECRET"),
        environment=env.get('environment_v')
    )
    
    # Register all routes
    register_routes(app)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 8090))

