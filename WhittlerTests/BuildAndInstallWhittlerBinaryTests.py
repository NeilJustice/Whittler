import platform
import unittest
from unittest.mock import call, patch
import docopt
from Whittler import Process
from WhittlerTests import BuildAndInstallWhittlerBinary, Random, UnitTester

testNames = [
'test_docstring_ReturnsExpected',
'test_docstring_ReturnsExpected',
'test_main_OSIsWindows_RunsPyinstallerToCreateWhittlerDotExe_CopiesWhittlerDotExeToInstallDirectory',
'test_main_OSIsLinux_RunsPyinstallerToCreateBinarywhittler_CopieswhittlerToInstallDirectory',
]

class BuildAndInstallWhittlerBinaryTests(unittest.TestCase):

   def test_docstring_ReturnsExpected(self):
      self.assertEqual("""BuildAndInstallWhittlerBinary.py
Builds binary 'whittler' on Linux or executable 'Whittler.exe' on Windows and then copies the Whittler binary file to --install-directory.

Usage: BuildAndInstallWhittlerBinary.py --install-directory=<DirectoryPath>""",
BuildAndInstallWhittlerBinary.__doc__)

   @patch('docopt.docopt', spec_set=True)
   @patch('platform.system', spec_set=True)
   @patch('builtins.print', spec_set=True)
   @patch('Whittler.Process.fail_fast_run', spec_set=True)
   def test_main_OSIsWindows_RunsPyinstallerToCreateWhittlerDotExe_CopiesWhittlerDotExeToInstallDirectory(self, _1, printMock, _3, _4):
      installDirectoryPath = Random.string()
      docopt.docopt.return_value =\
      {
         '--install-directory': installDirectoryPath
      }
      platform.system.return_value = 'Windows'
      #
      BuildAndInstallWhittlerBinary.main()
      #
      docopt.docopt.assert_called_once_with(BuildAndInstallWhittlerBinary.__doc__)
      platform.system.assert_called_once_with()
      self.assertEqual(4, len(printMock.call_args_list))
      printMock.assert_has_calls([
         call(f'[BuildAndInstallWhittlerBinary.py] --install-directory={installDirectoryPath}'),
         call("[BuildAndInstallWhittlerBinary.py] Building binary 'Whittler.exe' with pyinstaller..."),
         call(f"[BuildAndInstallWhittlerBinary.py] Successfully built and copied Whittler binary 'Whittler.exe' to install directory {installDirectoryPath}"),
         call('[BuildAndInstallWhittlerBinary.py] ExitCode: 0')])
      expectedPyinstallerCommandLine = f"pyinstaller Whittler/WhittlerMain.py --onefile -n Whittler.exe --distpath {installDirectoryPath} --log-level ERROR --version-file Whittler/WhittlerWindowsVersionForPyinstaller.txt"
      Process.fail_fast_run.assert_called_once_with(expectedPyinstallerCommandLine, False)

   @patch('docopt.docopt', spec_set=True)
   @patch('platform.system', spec_set=True)
   @patch('builtins.print', spec_set=True)
   @patch('Whittler.Process.fail_fast_run', spec_set=True)
   def test_main_OSIsLinux_RunsPyinstallerToCreateBinarywhittler_CopieswhittlerToInstallDirectory(self, _1, printMock, _3, _4):
      installDirectoryPath = Random.string()
      docopt.docopt.return_value =\
      {
         '--install-directory': installDirectoryPath
      }
      platform.system.return_value = 'Linux'
      #
      BuildAndInstallWhittlerBinary.main()
      #
      docopt.docopt.assert_called_once_with(BuildAndInstallWhittlerBinary.__doc__)
      platform.system.assert_called_once_with()
      self.assertEqual(4, len(printMock.call_args_list))
      printMock.assert_has_calls([
         call(f'[BuildAndInstallWhittlerBinary.py] --install-directory={installDirectoryPath}'),
         call("[BuildAndInstallWhittlerBinary.py] Building binary 'whittler' with pyinstaller..."),
         call(f"[BuildAndInstallWhittlerBinary.py] Successfully built and copied Whittler binary 'whittler' to install directory {installDirectoryPath}"),
         call('[BuildAndInstallWhittlerBinary.py] ExitCode: 0')])
      expectedPyinstallerCommandLine = f"pyinstaller Whittler/WhittlerMain.py --onefile -n whittler --distpath {installDirectoryPath} --log-level ERROR"
      Process.fail_fast_run.assert_called_once_with(expectedPyinstallerCommandLine, False)

if __name__ == '__main__': # pragma nocover
   UnitTester.run_tests(BuildAndInstallWhittlerBinaryTests, testNames)
