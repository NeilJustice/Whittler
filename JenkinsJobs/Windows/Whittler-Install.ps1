$env:PYTHONPATH = '.'
python.exe -u WhittlerTests\BuildAndInstallWhittlerBinary.py --install-directory=C:\bin
exit $LastExitCode
