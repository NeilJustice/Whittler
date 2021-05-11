#!/bin/bash
set -v

export PYTHONPATH=.
python WhittlerTests/BuildAndInstallWhittlerBinary.py --install-directory=/usr/local/bin
