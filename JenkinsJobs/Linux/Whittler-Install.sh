#!/bin/bash
set -v

export PYTHONPATH=.
python -u WhittlerTests/BuildAndInstallWhittlerBinary.py --install-directory=/usr/local/bin
