import re

from config import MAX_URL_LENGTH

_SCHEME = re.compile(r"^[a-z][a-z0-9+.\-]*://", re.IGNORECASE)


class InvalidURL(ValueError):
    """The user's input cannot be turned into a URL the model understands."""


def clean_url(raw) -> str:
    """Make user input look like the training data.

    Training URLs have no scheme ("https://"), and the hand-crafted features
    (host, path, slash count) rely on that, so we strip it here. Lowercasing and
    tokenizing are done by the model pipeline itself (see url_utils.py).
    """
    url = _SCHEME.sub("", str(raw or "").strip().strip("\"'<>"))

    if not url:
        raise InvalidURL("Enter a URL to check.")
    if re.search(r"\s", url):
        raise InvalidURL("A URL cannot contain spaces.")
    if "." not in url:
        raise InvalidURL("That doesn't look like a URL. Try something like example.com/login.")
    if len(url) > MAX_URL_LENGTH:
        raise InvalidURL(f"URL is too long (max {MAX_URL_LENGTH} characters).")
    return url
