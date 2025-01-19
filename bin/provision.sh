#!/usr/bin/env bash

set -e

if command -v uv; then
    uvx pyinfra -y inventory.py main.py "$@"
else
    pyinfra -y inventory.py main.py "$@"
fi
