import math

import joblib
import pandas as pd

from config import BORDERLINE_MARGIN, MODEL_PATH

from .url_cleaning import clean_url
from .url_utils import url_tokenizer


class PhishingPredictor:
    """Loads the trained pipeline once and turns raw user input into a verdict."""

    def __init__(self, model_path=MODEL_PATH):
        self.model = joblib.load(model_path)

    def predict(self, raw_url: str) -> dict:
        url = clean_url(raw_url)  # same shape as the training data
        score = float(self.model.decision_function(pd.Series([url]))[0])

        return {
            "cleaned_url": url,
            "tokens": url_tokenizer(url),
            "is_phishing": score > 0,
            "borderline": abs(score) < BORDERLINE_MARGIN,
            "score": score,
            "risk": 1 / (1 + math.exp(-score)),  # 0-1 display value, not a calibrated probability
        }
