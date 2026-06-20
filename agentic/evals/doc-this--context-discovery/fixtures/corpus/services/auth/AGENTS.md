# Auth — agent instructions

This folder has no README of its own; for service-wide context read the parent
[services README](../README.md). These are the rules you **must** follow when
working here.

## How to add or change a token type

Token definitions are **generated**. Never hand-edit `tokens.py` — it is
overwritten on every build, so your changes will be lost. To add or change a
token type, edit `token_types.yaml` and run `python gen_tokens.py`, which
regenerates `tokens.py`.
