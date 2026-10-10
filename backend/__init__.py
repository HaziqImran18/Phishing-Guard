from flask import Flask

from .predictor import PhishingPredictor
from .routes import bp


def create_app() -> Flask:
    # Templates and static files live in ../frontend so UI and API code stay separate.
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static",
    )
    app.extensions["predictor"] = PhishingPredictor()  # model is loaded once at startup
    app.register_blueprint(bp)
    return app
