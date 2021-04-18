$env:PYTHONPATH = '.'
python.exe -u WhittlerTests\MypyFlake8PylintRunTestsWithCoverage.py --run-tests-with-coverage-python-file=WhittlerTests/RunAllWithCoverage.py
exit $LastExitCode
