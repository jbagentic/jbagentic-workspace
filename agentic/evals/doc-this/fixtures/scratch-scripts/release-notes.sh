#!/usr/bin/env bash
# Print the git log since the last tag as markdown bullets.
set -euo pipefail
last_tag=$(git describe --tags --abbrev=0)
git log "${last_tag}..HEAD" --pretty='- %s'
