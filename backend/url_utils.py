import re
from functools import lru_cache

import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer

_tokenizer = RegexpTokenizer(r"[A-Za-z]+")
_stemmer = SnowballStemmer("english")

# Ye words dono classes mein common hain, koi signal nahi dete
URL_STOPWORDS = {"www", "com", "http", "https"}

SUSPICIOUS_WORDS = (
    "login", "signin", "secure", "verify", "account", "update", "bank",
    "paypal", "confirm", "password", "webscr", "ebay", "banking", "cmd",
)
IP_PATTERN = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}")


@lru_cache(maxsize=None)
def _stem(word):
    return _stemmer.stem(word)


def url_tokenizer(url):
    """lowercase -> sirf letters -> stopwords/1-letter tokens hatao -> stem."""
    tokens = _tokenizer.tokenize(str(url).lower())
    return [_stem(t) for t in tokens if t not in URL_STOPWORDS and len(t) > 1]


def extract_features(urls):
    """Hand-crafted numeric features. Input: list/Series of URLs."""
    rows = []
    for url in pd.Series(urls).astype(str):
        u = url.lower()
        host = u.split("/")[0].split("?")[0]
        path = u[len(host):]
        digits = sum(ch.isdigit() for ch in u)
        rows.append([
            len(u),                                    # total length
            len(host),                                 # host length
            len(path),                                 # path length
            host.count("."),                           # dots in host (subdomains)
            u.count("."),                              # total dots
            u.count("-"),                              # hyphens
            u.count("_"),                              # underscores
            u.count("/"),                              # slashes (path depth)
            u.count("?"),
            u.count("="),
            u.count("&"),
            u.count("%"),
            int("@" in u),                             # '@' trick
            int(bool(IP_PATTERN.match(u))),            # IP address as host
            digits,                                    # digit count
            digits / max(len(u), 1),                   # digit ratio
            sum(u.count(w) for w in SUSPICIOUS_WORDS), # suspicious keywords
        ])
    return np.log1p(np.array(rows, dtype=float))
