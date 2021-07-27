$originalPythonPath = $env:PYTHONPATH
$env:PYTHONPATH="."
python.exe WhittlerTests\MypyFlake8PylintRunTestsWithCoverage.py --run-tests-with-coverage-python-file=WhittlerTests/RunAllWithCoverage.py
$env:PYTHONPATH=$originalPythonPath
exit $LastExitCode
