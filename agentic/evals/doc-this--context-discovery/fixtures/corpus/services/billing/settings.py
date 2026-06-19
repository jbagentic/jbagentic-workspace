# Billing runtime configuration — the source of truth for retry behavior.
# Loaded by handler.py at startup.

RETRY_ATTEMPTS = 3              # retry a failed capture up to 3 times
RETRY_BACKOFF = "exponential"  # 1s, 2s, 4s between attempts
