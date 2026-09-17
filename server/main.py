"""
s0P0wn3d C2 Server — entry point
T1071: Application Layer Protocol (HTTPS)
"""
import ssl
from pathlib import Path

from flask import Flask
from api.routes import register_routes

CERT = Path(__file__).parent.parent / "certs" / "cert.pem"
KEY  = Path(__file__).parent.parent / "certs" / "key.pem"
HOST = "0.0.0.0"
PORT = 443


def create_app() -> Flask:
    app = Flask(__name__)
    register_routes(app)
    return app


if __name__ == "__main__":
    app = create_app()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(str(CERT), str(KEY))
    app.run(host=HOST, port=PORT, ssl_context=context, debug=False)
