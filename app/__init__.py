from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from app.config import DevConfig


def create_app(config):
    """Construct the core application."""
    app = Flask(__name__, static_url_path=config.ROOT_URL + '/static', instance_relative_config=False)
    app.config.from_object(config)
    # CORS(app, resources={r"/*": {"origins": "*"}})
    if config == DevConfig:
        DebugToolbarExtension(app)

    return app


app = create_app(config=DevConfig)

from app import views
