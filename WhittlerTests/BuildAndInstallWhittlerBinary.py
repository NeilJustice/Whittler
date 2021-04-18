"""BuildAndInstallWhittlerBinary.py
Builds binary 'whittler' on Linux or executable 'Whittler.exe' on Windows and then copies the Whittler binary file to --install-directory.

Usage: BuildAndInstallWhittlerBinary.py --install-directory=<DirectoryPath>"""
import platform
import docopt
from Whittler import Process

def main() -> None:
   arguments = docopt.docopt(__doc__)
   installDirectoryPath = arguments['--install-directory']
   print(f'[BuildAndInstallWhittlerBinary.py] --install-directory={installDirectoryPath}')
   platformSystem = platform.system()
   if platformSystem.casefold() == 'windows':
      whittlerBinaryName = 'Whittler.exe'
      pyinstallerCommandLine = f"pyinstaller Whittler/WhittlerMain.py --onefile -n {whittlerBinaryName} --distpath {installDirectoryPath} --log-level ERROR --version-file Whittler/WhittlerWindowsVersionForPyinstaller.txt"
   else:
      whittlerBinaryName = 'whittler'
      pyinstallerCommandLine = f"pyinstaller Whittler/WhittlerMain.py --onefile -n {whittlerBinaryName} --distpath {installDirectoryPath} --log-level ERROR"
   print(f"[BuildAndInstallWhittlerBinary.py] Building binary '{whittlerBinaryName}' with pyinstaller...")
   Process.fail_fast_run(pyinstallerCommandLine, False)
   print(f"[BuildAndInstallWhittlerBinary.py] Successfully built and copied Whittler binary '{whittlerBinaryName}' to install directory {installDirectoryPath}")
   print('[BuildAndInstallWhittlerBinary.py] ExitCode: 0')

if __name__ == '__main__': # pragma nocover
   main()

# Example Windows command line:
# --install-directory=C:\bin
# Working directory: D:\Code\Whittler

# Example Linux command line:
# --install-directory=/usr/local/bin
# Working directory: /code/Whittler
