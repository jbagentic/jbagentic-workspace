#!/usr/bin/env bash
# deploy.sh — build and deploy all services to the staging cluster.
set -euo pipefail

build_all_services
push_images
apply_manifests --env staging
