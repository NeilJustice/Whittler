import glob
import os
import platform
import sys
import unittest
from unittest.mock import call, patch
from Whittler import Process
from WhittlerTests import ParallelProcess, Python, Random, UnitTester

testNames = [
'test_run_flake8_RunsFlake8WithFlake8Config',
'test_run_mypy_RunsMypyDotWithIgnoreMissingImports',
'test_run_pylint_on_file_CallsPylintOnAllPythonFilesInCurrentFolderAndSubFolders',
'test_run_pylint_on_all_files_in_parallel_LinuxCallsMapParallelPylintFileWithAllPyFilePaths_WindowsCallsMapSequential',
'test_run_all_with_coverage_RunsCoverage_RunsReport_RunsHtml_RunsXml_ExitsWithReportExitCode'
]

class PythonTests(unittest.TestCase):

   ExpectedPylintCommand = 'pylint --rcfile=.pylintrc --score=n '

   @staticmethod
   @patch('Whittler.Process.fail_fast_run', spec_set=True)
   def test_run_flake8_RunsFlake8WithFlake8Config(_1):
      #
      Python.run_flake8()
      #
      expectedFlake8Command = 'flake8 --config=.flake8 --show-source --benchmark'
      Process.fail_fast_run.assert_called_once_with(expectedFlake8Command, False)

   @staticmethod
   @patch('Whittler.Process.fail_fast_run', spec_set=True)
   def test_run_mypy_RunsMypyDotWithIgnoreMissingImports(_1):
      #
      Python.run_mypy()
      #
      expectedMypyCommand = 'mypy .'
      Process.fail_fast_run(expectedMypyCommand, False)

   @patch('Whittler.Process.run_and_get_exit_code', spec_set=True)
   def test_run_pylint_on_file_CallsPylintOnAllPythonFilesInCurrentFolderAndSubFolders(self, _1):
      pylintExitCode = Random.integer()
      Process.run_and_get_exit_code.return_value = pylintExitCode
      pythonFilePath = Random.string()
      #
      pylintExitCode = Python.run_pylint_on_file(pythonFilePath)
      #
      Process.run_and_get_exit_code.assert_called_once_with(PythonTests.ExpectedPylintCommand + pythonFilePath, False)
      self.assertEqual(pylintExitCode, pylintExitCode)

   def test_run_pylint_on_all_files_in_parallel_LinuxCallsMapParallelPylintFileWithAllPyFilePaths_WindowsCallsMapSequential(self):
      @patch('glob.glob', spec_set=True)
      @patch('platform.system', spec_set=True)
      @patch('WhittlerTests.ParallelProcess.run_parallel_processpoolexecutor', spec_set=True)
      @patch('WhittlerTests.ParallelProcess.run_parallel_processthread', spec_set=True)
      @patch('sys.exit', spec_set=True)
      def testcase(platformSystem, expectedMapParallel, allPylintProcessesSucceeded, expectSysExit1, _1, _2, _3, _4, _5):
         with self.subTest(f'{platformSystem, expectedMapParallel, allPylintProcessesSucceeded, expectSysExit1}'):
            PyFilePaths = [Random.string(), Random.string()]
            glob.glob.return_value = PyFilePaths
            platform.system.return_value = platformSystem
            if expectedMapParallel:
               ParallelProcess.run_parallel_processpoolexecutor.return_value = allPylintProcessesSucceeded
            else:
               ParallelProcess.run_parallel_processthread.return_value = allPylintProcessesSucceeded
            #
            Python.run_pylint_on_all_files_in_parallel()
            #
            glob.glob.assert_called_once_with('**/*.py', recursive=True)
            platform.system.assert_called_once_with()
            if expectedMapParallel:
               ParallelProcess.run_parallel_processpoolexecutor.assert_called_once_with(Python.run_pylint_on_file, PyFilePaths)
               ParallelProcess.run_parallel_processthread.assert_not_called()
            else:
               ParallelProcess.run_parallel_processpoolexecutor.assert_not_called()
               ParallelProcess.run_parallel_processthread.assert_called_once_with(PythonTests.ExpectedPylintCommand, PyFilePaths)
            if expectSysExit1:
               sys.exit.assert_called_once_with(1)
            else:
               sys.exit.assert_not_called()
      testcase('Linux', True, True, False)
      testcase('Windows', False, False, True)
      testcase('windows', True, False, True)

   def test_run_all_with_coverage_RunsCoverage_RunsReport_RunsHtml_RunsXml_ExitsWithReportExitCode(self):
      @patch('os.getcwd', spec_set=True)
      @patch('Whittler.Process.fail_fast_run', spec_set=True)
      @patch('Whittler.Process.run_and_get_exit_code', spec_set=True)
      @patch('sys.exit', spec_set=True)
      @patch('builtins.print', spec_set=True)
      def testcase(reportExitCode, expectedConcludingPrint, printMock, _2, _3, _4, _5):
         currentWorkingDirectory = Random.string()
         os.getcwd.return_value = currentWorkingDirectory
         Process.run_and_get_exit_code.return_value = reportExitCode
         testsProjectName = Random.string()
         omitPattern = Random.string()
         #
         Python.run_all_tests_with_coverage(testsProjectName, omitPattern)
         #
         self.assertEqual(2, len(printMock.call_args_list))
         printMock.assert_has_calls([call(f'Running {testsProjectName}/RunAll.py with coverage from', currentWorkingDirectory)])
         Process.run_and_get_exit_code.assert_called_once_with(f'coverage report --omit="{omitPattern}" --fail-under=100 --show-missing', False)
         self.assertEqual(3, len(Process.fail_fast_run.call_args_list))
         Process.fail_fast_run.assert_has_calls([
            call(f'coverage run --branch {testsProjectName}/RunAll.py', False),
            call(f'coverage xml --omit="{omitPattern}" -o {testsProjectName}/CoberturaCodeCoverageResults_{testsProjectName}.xml', False),
            call(f'coverage html --omit="{omitPattern}" --directory={testsProjectName}/CodeCoverageHTMLReport --title="{testsProjectName} Code Coverage"', False)])
         printMock.assert_has_calls([call(expectedConcludingPrint)])
         sys.exit.assert_called_once_with(reportExitCode)
      expectedFailureMessage = 'Failure. Code coverage is less than 100%.'
      testcase(-1, expectedFailureMessage)
      testcase(0, 'Success. Code coverage is 100%.')
      testcase(1, expectedFailureMessage)
      testcase(2, expectedFailureMessage)

if __name__ == '__main__': # pragma nocover
   UnitTester.run_tests(PythonTests, testNames)
