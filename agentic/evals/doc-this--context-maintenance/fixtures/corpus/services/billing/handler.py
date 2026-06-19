# Payment capture handler. Reads retry settings from config.py.
from config import RETRY_ATTEMPTS, RETRY_BACKOFF


def capture(payment):
    """Capture a payment, retrying a failed attempt per config."""
    for attempt in range(RETRY_ATTEMPTS):
        if _try_capture(payment):
            return True
    return False


def _try_capture(payment):
    raise NotImplementedError
