from flask import Flask
from src.config import Config
from src.db import db
from src.routes.health import health_bp
from src.routes.users import users_bp


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(users_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
