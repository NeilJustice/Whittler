$originalPythonPath = $env:PYTHONPATH
$env:PYTHONPATH="."
python.exe WhittlerTests\BuildAndInstallWhittlerBinary.py --install-directory=C:\bin
$env:PYTHONPATH=$originalPythonPath
exit $LastExitCode
