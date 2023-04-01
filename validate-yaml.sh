#!/usr/bin/env bash
set -euo pipefail

# validate yaml files with yaml-lint
find deployment -name '*.yaml' -exec python -m yamllint -c .yamllint.yaml {} +
