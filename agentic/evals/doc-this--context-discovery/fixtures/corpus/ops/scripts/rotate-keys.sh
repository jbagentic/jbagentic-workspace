#!/usr/bin/env bash
# rotate-keys.sh — rotate the API signing keys.
#
# Generates a fresh signing key, publishes it to the key store, marks the
# previous key as "retiring" (still accepted for 24h so in-flight requests keep
# verifying), then revokes any key older than 24h. Meant to run weekly via cron.
set -euo pipefail

new_key="$(generate_signing_key)"
publish_to_keystore "$new_key"
mark_previous_retiring
revoke_keys_older_than "24h"
