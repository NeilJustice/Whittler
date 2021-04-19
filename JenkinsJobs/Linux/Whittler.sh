#!/bin/bash
set -v
PYTHONPATH=.
python -u WhittlerTests/MypyFlake8PylintRunTestsWithCoverage.py --run-tests-with-coverage-python-file=WhittlerTests/RunAllWithCoverage.py
