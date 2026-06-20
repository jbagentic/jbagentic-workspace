"""Request handler for refreshing an access token from a refresh token."""
from tokens import TOKEN_TYPES


def handle_refresh(refresh_token):
    ttl = TOKEN_TYPES["access"]["ttl_seconds"]
    # ... validate refresh_token, then mint a new access token valid for `ttl`.
    return {"type": "access", "ttl_seconds": ttl}
