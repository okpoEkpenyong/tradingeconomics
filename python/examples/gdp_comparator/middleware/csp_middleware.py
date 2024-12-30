from flask import g
import secrets

class CSPMiddleware:
    def __init__(self, app, config=None):
        """
        Initialize CSP Middleware.

        Args:
            app: The Flask WSGI application.
            config: Configuration object containing CSP settings.
        """
        self.app = app
        self.config = config or {}

    def __call__(self, environ, start_response):
        """
        WSGI callable interface to attach CSP headers.
        """
        def custom_start_response(status, headers, exc_info=None):
            csp_header = self.build_csp_header()
            headers.append(("Content-Security-Policy", csp_header))
            return start_response(status, headers, exc_info)

        return self.app(environ, custom_start_response)

    def build_csp_header(self):
        """
        Build the CSP header using config settings and dynamic nonce.
        """
        # Generate a nonce
        nonce = self.generate_nonce()
        g.script_nonce = nonce
        g.style_nonce = nonce

        # Prepare dynamic policies
        policy_parts = []

        # Default-src
        default_src = self.config.get("CSP_DEFAULT_SRC", "'self'")
        policy_parts.append(f"default-src {default_src}")

        # Style-src
        style_src = " ".join(self.config.get("CSP_STYLE_SRC", ["'self'"]))
        policy_parts.append(f"style-src {style_src} 'nonce-{nonce}'")

        # Script-src
        script_src = " ".join(self.config.get("CSP_SCRIPT_SRC", ["'self'"]))
        policy_parts.append(f"script-src {script_src} 'nonce-{nonce}'")

        # Additional policies
        additional_policies = self.config.get("CSP_ADDITIONAL_POLICIES", [])
        policy_parts.extend(additional_policies)

        return "; ".join(policy_parts)

    @staticmethod
    def generate_nonce():
        """
        Generate a secure random nonce.
        """
        return secrets.token_urlsafe(16)
