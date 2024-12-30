# app/extensions.py
from flask_cors import CORS
from flask_compress import Compress
from flask_talisman import Talisman
from flask_caching import Cache
from middleware.csp_middleware import CSPMiddleware

# Initialize extensions
cors = CORS()
compress = Compress()
talisman = Talisman()
cache = Cache()


def init_extensions(app):
    """Attach extensions and middleware to the Flask app."""
    cors.init_app(app)
    compress.init_app(app)
    cache.init_app(app)
   
    # Map custom config keys to Talisman-compatible CSP directives
    csp_config = {
        "default-src": app.config.get("CSP_DEFAULT_SRC", "'self'"),
        "style-src": app.config.get("CSP_STYLE_SRC", ["'self'"]),
        "script-src": app.config.get("CSP_SCRIPT_SRC", ["'self'"]),
    }

    # Add additional policies
    additional_policies = app.config.get("CSP_ADDITIONAL_POLICIES", [])
    for policy in additional_policies:
        directive, sources = policy.split(" ", 1)
        if directive in csp_config:
            # Merge with existing sources
            csp_config[directive] = csp_config[directive] + " " + sources
        else:
            # Add new directive
            csp_config[directive] = sources

    # Initialize Talisman with the constructed CSP
    talisman.init_app(app, content_security_policy=csp_config)
    
    
    
