$env:PYTHONPATH="."
python.exe WhittlerTests\MypyFlake8PylintRunTestsWithCoverage.py --run-tests-with-coverage-python-file=WhittlerTests/RunAllWithCoverage.py
exit $LastExitCode
