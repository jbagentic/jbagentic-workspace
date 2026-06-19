# Auth — agent notes

## Conventions

- Token helpers live in `session_tokens.py`. Import `issue_access_token` and
  `issue_refresh_token` from there — don't put token logic in `login.py`.
