#!/usr/bin/env bash

set -e

PYINFRA_INVENTORY="${1:-inventory.py}"

if command -v uv; then
    uvx pyinfra -y "${PYINFRA_INVENTORY}" main.py "$@"
else
    pyinfra -y "${PYINFRA_INVENTORY}" main.py "$@"
fi
