"""Payment capture handler for the billing service."""

from settings import RETRY_ATTEMPTS, RETRY_BACKOFF


def capture(payment):
    """Attempt to capture a payment, retrying per the configured policy."""
    for attempt in range(RETRY_ATTEMPTS):
        if _try_capture(payment):
            emit("billing.payment.captured", payment)
            return True
        _wait(RETRY_BACKOFF, attempt)
    emit("billing.payment.failed", payment)
    return False


def _try_capture(payment):  # placeholder
    ...


def _wait(backoff, attempt):  # placeholder
    ...


def emit(event_name, payload):  # placeholder
    ...
