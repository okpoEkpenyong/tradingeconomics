from flask import Flask, redirect
from extensions import init_extensions
from service.api_client import APIClient
from routes.api import api_bp
from config.settings import Config
from errors import register_error_handlers


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_error_handlers(app)
    
    # Initialize extensions and middleware
    init_extensions(app)

    # Root-level redirection
    @app.route('/')
    def redirect_to_api():
        return redirect('/api/')

    # Register Blueprints
    app.register_blueprint(api_bp, url_prefix="/api")

    return app

# Expose the global app for Gunicorn to access
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
