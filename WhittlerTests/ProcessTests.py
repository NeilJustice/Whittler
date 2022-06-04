import concurrent.futures
import multiprocessing
import platform
import shlex
import sys
import subprocess
import unittest
from unittest.mock import patch, call
from Whittler import Process
from WhittlerTests import ParallelProcess, Random, UnitTester

testNames = [
'test_append_args_AppendsSpaceThenArgsIfArgsNotEmpty',
'test_cross_platform_subprocess_call_Windows_RunInBackgroundIfWindowsIsFalse_CallsSubprocessCall_ReturnsExitCode',
'test_cross_platform_subprocess_call_Windows_RunInBackgroundIfWindowsIsTrue_CallsSubprocessPopen_Returns0',
'test_cross_platform_subprocess_call_Linux_CallsSubprocessCallWithShlexedCommand_ReturnsSubprocessCallReturnValue',
'test_fail_fast_run_CallsProcessAndGetExitCode_SysExitsWithExitCodeIfRunReturnsNonZero',
'test_run_and_get_exit_code_RunsProcess_ReturnsExitCode',
'test_run_and_get_exit_code_RunsProcess_ProcessRaisesAnException_PrintsException_Exits1',
'test_run_parallel_processpoolexecutor_CallsProcessPoolExecutorMap_Returns1IfAnyExitCodesNon0',
'test_run_SubprocessRunsProcessWithCheckEqualsFalse_ReturnsStdOutStdErr'
]

class ProcessTests(unittest.TestCase):
   def setUp(self):
      self.configuration = Random.string()
      self.projectName = Random.string()
      self.appendArgsReturnValue = Random.string()
      self.command = Random.string()
      self.shlexedCommand = Random.string()
      self.currentWorkingDirectory = Random.string()
      self.ExpectedPylintcommand = 'pylint --rcfile=.pylintrc '

   @patch('platform.system', spec_set=True)
   @patch('subprocess.call', spec_set=True)
   def test_cross_platform_subprocess_call_Windows_RunInBackgroundIfWindowsIsFalse_CallsSubprocessCall_ReturnsExitCode(self, _1, _2):
      platform.system.return_value = 'Windows'
      subprocessCallReturnValue = Random.integer()
      subprocess.call.return_value = subprocessCallReturnValue
      #
      exitCode = Process.cross_platform_subprocess_call(self.command, False)
      #
      platform.system.assert_called_once_with()
      subprocess.call.assert_called_once_with(self.command)
      self.assertEqual(subprocessCallReturnValue, exitCode)

   @patch('platform.system', spec_set=True)
   @patch('subprocess.Popen', spec_set=True)
   def test_cross_platform_subprocess_call_Windows_RunInBackgroundIfWindowsIsTrue_CallsSubprocessPopen_Returns0(self, _1, _2):
      platform.system.return_value = 'Windows'
      #
      exitCode = Process.cross_platform_subprocess_call(self.command, True)
      #
      platform.system.assert_called_once_with()
      subprocess.Popen.assert_called_once_with(self.command)
      self.assertEqual(0, exitCode)

   @patch('platform.system', spec_set=True)
   @patch('shlex.split', spec_set=True)
   @patch('subprocess.call', spec_set=True)
   def test_cross_platform_subprocess_call_Linux_CallsSubprocessCallWithShlexedCommand_ReturnsSubprocessCallReturnValue(self, _1, _2, _3):
      platform.system.return_value = 'Linux'
      shlex.split.return_value = self.shlexedCommand
      subprocessCallReturnValue = Random.integer()
      subprocess.call.return_value = subprocessCallReturnValue
      runInBackgroundIfWindows = Random.boolean()
      #
      exitCode = Process.cross_platform_subprocess_call(self.command, runInBackgroundIfWindows)
      #
      platform.system.assert_called_once_with()
      subprocess.call.assert_called_once_with(self.shlexedCommand)
      self.assertEqual(subprocessCallReturnValue, exitCode)

   def test_append_args_AppendsSpaceThenArgsIfArgsNotEmpty(self):
      def testcase(expectedReturnValue: str, args: str) -> None:
         with self.subTest(f'{expectedReturnValue, args}'):
            returnValue = Process.append_args('ExePath', args)
            self.assertEqual(expectedReturnValue, returnValue)
      testcase('ExePath', '')
      testcase('ExePath  ', ' ')
      testcase('ExePath arg1', 'arg1')
      testcase('ExePath arg1 arg2', 'arg1 arg2')

   def test_fail_fast_run_CallsProcessAndGetExitCode_SysExitsWithExitCodeIfRunReturnsNonZero(self):
      @patch('Whittler.Process.run_and_get_exit_code', spec_set=True)
      @patch('builtins.print', spec_set=True)
      @patch('sys.exit', spec_set=True)
      def testcase(exitCode, expectPrintCommandFailedAndExit, _1, printMock, _3):
         with self.subTest(f'{exitCode, expectPrintCommandFailedAndExit}'):
            Process.run_and_get_exit_code.return_value = exitCode
            runInBackgroundIfWindows = Random.boolean()
            #
            Process.fail_fast_run(self.command, runInBackgroundIfWindows)
            #
            Process.run_and_get_exit_code.assert_called_once_with(self.command, runInBackgroundIfWindows)
            if expectPrintCommandFailedAndExit:
               expectedSingleQuotedCommand = f'\'{self.command}\''
               printMock.assert_called_once_with('Command', expectedSingleQuotedCommand, 'failed with exit code', exitCode)
               sys.exit.assert_called_once_with(exitCode)
            else:
               sys.exit.assert_not_called()
      testcase(-1, True)
      testcase(0, False)
      testcase(1, True)

   @patch('shlex.split', spec_set=True)
   @patch('subprocess.run', spec_set=True)
   def test_run_SubprocessRunsProcessWithCheckEqualsFalse_ReturnsStdOutStdErr(self, _1, _2):
      shlex.split.return_value = self.shlexedCommand
      args = [Random.string(), Random.string()]
      returncode = Random.integer()
      stdoutUtf8 = Random.string()
      stderrUtf8 = Random.string()
      stdoutBytes = stdoutUtf8.encode('utf-8')
      stderrBytes = stderrUtf8.encode('utf-8')
      subprocessRunReturnValue = subprocess.CompletedProcess(args, returncode, stdoutBytes, stderrBytes)
      subprocess.run.return_value = subprocessRunReturnValue
      #
      (stdout, stderr) = Process.run(self.command)
      #
      shlex.split.assert_called_once_with(self.command)
      subprocess.run.assert_called_once_with(self.shlexedCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
      self.assertEqual(stdoutUtf8, stdout)
      self.assertEqual(stderrUtf8, stderr)

   @patch('builtins.print', spec_set=True)
   @patch('Whittler.Process.cross_platform_subprocess_call', spec_set=True)
   def test_run_and_get_exit_code_RunsProcess_ReturnsExitCode(self, _1, printMock):
      subprocessReturnValue = Random.integer()
      Process.cross_platform_subprocess_call.return_value = subprocessReturnValue
      runInBackgroundIfWindows = Random.boolean()
      #
      exitCode = Process.run_and_get_exit_code(self.command, runInBackgroundIfWindows)
      #
      printMock.assert_called_once_with(' Running:', f'\'{self.command}\'')
      Process.cross_platform_subprocess_call.assert_called_once_with(self.command, runInBackgroundIfWindows)
      self.assertEqual(subprocessReturnValue, exitCode)

   @patch('builtins.print', spec_set=True)
   @patch('Whittler.Process.cross_platform_subprocess_call', spec_set=True)
   @patch('sys.exit', spec_set=True)
   def test_run_and_get_exit_code_RunsProcess_ProcessRaisesAnException_PrintsException_Exits1(self, _1, _2, printMock):
      exceptionMessage = Random.string()
      Process.cross_platform_subprocess_call.side_effect = FileNotFoundError(exceptionMessage)
      runInBackgroundIfWindows = Random.boolean()
      #
      Process.run_and_get_exit_code(self.command, runInBackgroundIfWindows)
      #
      Process.cross_platform_subprocess_call.assert_called_once_with(self.command, runInBackgroundIfWindows)
      self.assertEqual(2, len(printMock.call_args_list))
      printMock.assert_has_calls([
         call(' Running:', f'\'{self.command}\''),
         call(exceptionMessage)])
      sys.exit.assert_called_once_with(1)

   def test_run_parallel_processpoolexecutor_CallsProcessPoolExecutorMap_Returns1IfAnyExitCodesNon0(self):
      class ProcessPoolExecutorMock:
         def __init__(self):
            self.map_numberOfCalls = 0
            self.map_funcArg = None
            self.map_iterableArg = None
            self.map_returnValue = None
            self.shutdown_numberOfCalls = 0
            self.shutdown_waitArg = None

         def map(self, func, iterable):
            self.map_numberOfCalls = self.map_numberOfCalls + 1
            self.map_funcArg = func
            self.map_iterableArg = iterable
            return self.map_returnValue

         def shutdown(self, wait):
            self.shutdown_numberOfCalls = self.shutdown_numberOfCalls + 1
            self.shutdown_waitArg = wait

         def assert_map_called_once_with(self, expectedFunc, expectedIterable):
            assert self.map_numberOfCalls == 1
            assert expectedFunc, self.map_funcArg
            assert expectedIterable, self.map_iterableArg

         def assert_shutdown_called_once_with(self, expectedWait):
            assert 1, self.numberOfShutdownCalls
            assert expectedWait, self.shutdown_waitArg

      @patch('concurrent.futures.ProcessPoolExecutor', spec_set=True)
      @patch('multiprocessing.cpu_count', spec_set=True)
      def testcase(expectedReturnValue, exitCodes, _1, _2):
         with self.subTest(f'{expectedReturnValue, exitCodes}'):
            cpuCount = Random.integer()
            multiprocessing.cpu_count.return_value = cpuCount
            Iterable = ['a', 'b', 'c']
            processPoolExecutorMock = ProcessPoolExecutorMock()
            processPoolExecutorMock.map_returnValue = exitCodes
            concurrent.futures.ProcessPoolExecutor.return_value = processPoolExecutorMock
            #
            allCommandsExited0 = ParallelProcess.run_parallel_processpoolexecutor(len, Iterable)
            #
            multiprocessing.cpu_count.assert_called_once_with()
            concurrent.futures.ProcessPoolExecutor.assert_called_once_with(cpuCount)
            processPoolExecutorMock.assert_map_called_once_with(len, Iterable)
            processPoolExecutorMock.assert_shutdown_called_once_with(True)
            self.assertEqual(expectedReturnValue, allCommandsExited0)
      testcase(False, [-1])
      testcase(True, [0])
      testcase(True, [0, 0])
      testcase(False, [1])
      testcase(False, [2])
      testcase(False, [1, 0])
      testcase(False, [0, 1])
      testcase(False, [0, 1, 0])

if __name__ == '__main__': # pragma nocover
   UnitTester.run_tests(ProcessTests, testNames)
