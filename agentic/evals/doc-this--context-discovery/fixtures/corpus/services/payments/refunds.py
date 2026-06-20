"""Refund functions for the payments service."""


def refund(charge_id):
    """Reverse a charge against the gateway. Low-level — see AGENTS.md before use."""
    ...


def request_refund(charge_id):
    """Enqueue a refund for approval; the approval worker calls refund() later."""
    ...
