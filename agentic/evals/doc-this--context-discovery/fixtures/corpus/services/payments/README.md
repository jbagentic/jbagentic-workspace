# Payments service

Processes charges and issues refunds against the payment gateway.

Core functions live in [refunds.py](refunds.py): `refund(charge_id)` performs the
actual reversal against the gateway, and `request_refund(charge_id)` enqueues a
refund for review.

Events emitted by payments follow the platform
[event naming convention](../README.md#event-naming-convention).
