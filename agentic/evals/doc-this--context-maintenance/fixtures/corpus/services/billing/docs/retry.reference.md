# Retry behavior — reference

A failed payment capture is retried **3 attempts** with **exponential backoff**
(1s, 2s, 4s between attempts). The authoritative values live in
[../config.py](../config.py) — `RETRY_ATTEMPTS` and `RETRY_BACKOFF`. This reference
restates them for readers; keep it in sync when the config changes.
