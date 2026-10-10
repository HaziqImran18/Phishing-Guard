from flask import Blueprint, current_app, jsonify, render_template, request

from .url_cleaning import InvalidURL

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template("index.html")


@bp.get("/health")
def health():
    return jsonify(status="ok")


@bp.post("/api/predict")
def predict():
    payload = request.get_json(silent=True)
    url = payload.get("url", "") if isinstance(payload, dict) else ""

    try:
        result = current_app.extensions["predictor"].predict(url)
    except InvalidURL as error:
        return jsonify(error=str(error)), 400
    return jsonify(result)
