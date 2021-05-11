#!/bin/bash
set -v

export PYTHONPATH=.
python WhittlerTests/MypyFlake8PylintRunTestsWithCoverage.py --run-tests-with-coverage-python-file=WhittlerTests/RunAllWithCoverage.py
