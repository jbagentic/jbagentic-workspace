# Payments — agent instructions

Rules you **must** follow when working in this service.

## Refunds must go through the approval queue

Never call `refund()` directly from product code — a direct call bypasses fraud
review. All refunds **must** be submitted via `request_refund(charge_id)`, which
enqueues the refund for approval before it runs. Only the approval worker is
allowed to call `refund()`.
