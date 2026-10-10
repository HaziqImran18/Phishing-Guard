from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "backend" / "model" / "phishing_pipeline.pkl"

MAX_URL_LENGTH = 2048
BORDERLINE_MARGIN = 0.5  # |SVM score| below this means "the model is unsure"
