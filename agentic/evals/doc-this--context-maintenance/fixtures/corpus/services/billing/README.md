# Billing service

Charges customers and captures payments.

## Capture

A payment capture call times out after **10 seconds**; see
[capture/capture.py](capture/capture.py) (`CAPTURE_TIMEOUT`). The `capture/` folder
has no README of its own — capture behavior is documented here, in the parent.

## Retry

Retry behavior for failed captures is specified in
[docs/retry.reference.md](docs/retry.reference.md). The authoritative values live in
[config.py](config.py) (`RETRY_ATTEMPTS`, `RETRY_BACKOFF`).
