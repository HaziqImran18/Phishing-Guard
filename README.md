# Phishing-Guard
# Phishing URL Detector

Flask app that classifies a URL as phishing or legitimate (Linear SVM on TF-IDF tokens + hand-crafted URL features).

```
app.py              entry point (gunicorn app:app)
config.py           paths and thresholds
backend/            Flask routes, input cleaning, model loading, training-time url_utils.py
  model/            phishing_pipeline.pkl
frontend/           Jinja template + static CSS/JS only (no Python)
```

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py                                       # http://127.0.0.1:5000
```

## Deploy on Render (free)
1. Push this folder to a GitHub repo.
2. Render → New → Blueprint (or Web Service) → pick the repo. `render.yaml` sets everything:
   build `pip install -r requirements.txt`, start `gunicorn app:app`, Python 3.12.
3. Wait for the build; your URL is live. `/health` is used as the health check.

## How input is cleaned
Training URLs had no `https://`, so `backend/url_cleaning.py` strips scheme/quotes/spaces and validates input
before prediction. Lowercasing, tokenizing and stemming happen inside the saved pipeline (`url_utils.py`),
exactly as in training. The JS mirrors the light cleaning only for display; the server is the source of truth.

## Notes
- "Risk score" is a sigmoid of the SVM margin for display. It is **not** a calibrated probability.
- Keep `scikit-learn` pinned to the training version, or the `.pkl` may fail to load.
- If you retrain: `from backend.url_utils import ...` in the notebook before `joblib.dump`,
  so the pickle references `backend.url_utils` and loads here.
- Not a replacement for real security tools. Model errors exist (~97% test accuracy).
