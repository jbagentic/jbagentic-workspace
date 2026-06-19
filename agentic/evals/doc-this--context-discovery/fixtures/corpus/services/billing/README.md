# Billing service

Charges customers and retries failed payment captures.

## Retry policy

A failed capture is retried **3 times** with **exponential backoff** (1s, 2s, 4s).
The authoritative values live in [settings.py](settings.py) — `RETRY_ATTEMPTS`
and `RETRY_BACKOFF`. That file is the source of truth for retry behavior.

> ⚠️ `legacy_config.py` is **deprecated** and no longer loaded anywhere. It
> predates the current policy and its values (5 attempts, fixed delay) are wrong.
> Do not read retry behavior from it.

Events emitted by billing follow the platform
[event naming convention](../README.md#event-naming-convention).
