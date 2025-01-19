import logging
from flask import Flask
from .config import APP_PORT, APP_DEBUG
from .routes.analytics_routes import analytics_blueprint

def create_app():
    app = Flask(__name__)

    logging.basicConfig(
        level=logging.DEBUG if APP_DEBUG else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting Analytics Microservice...")

    app.register_blueprint(analytics_blueprint, url_prefix='/analytics')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=APP_PORT, debug=APP_DEBUG)