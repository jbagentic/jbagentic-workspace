# Single payment-capture call. No README in this folder — capture behavior is
# documented in the parent billing README (../README.md, "Capture").

CAPTURE_TIMEOUT = 10  # seconds before a capture call is abandoned


def capture_once(payment):
    """Attempt a single capture, abandoning after CAPTURE_TIMEOUT seconds."""
    raise NotImplementedError
