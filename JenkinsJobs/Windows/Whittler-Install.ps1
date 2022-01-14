$originalPythonPath = $env:PYTHONPATH
$env:PYTHONPATH="."
python.exe -u WhittlerTests\BuildAndInstallWhittlerBinary.py --install-directory=C:\bin
$env:PYTHONPATH=$originalPythonPath
exit $LastExitCode
