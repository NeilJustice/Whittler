import inspect
import os
import sys
import unittest
from unittest.mock import call, patch
from Whittler import File, Process, WhittlerProgram
from WhittlerTests import Random, UnitTester

testNames = [
'test_get_module_ReturnsWhittlerProgramModule',
'test_make_whittler_filepath_for_command_ReturnsHomeSlashDotWhittlerSlashProgramNameAndArgsDotTxt',
'test_open_whittler_file_with_editor_environment_variable_OpensFileWithEDITOR',
'test_prefix_command_with_powershell_dot_exe_if_command_is_get_help_ReturnsPowerShellPrefixedCommandIfGetHelp',
'test_open_or_create_whittler_file_WhittlerFileAlreadyExists_OpensItWithEDITOR',
'test_open_or_create_whittler_file_WhittlerFileDoesNotAlreadyExist_CreatesItAndOpensItWithEDITOR',
'test_run_CallsOpenOrCreateWhittlerFile_Returns0',
'test_split_lines_and_remove_leading_and_trailing_whitespace_and_carriage_returns',
'test_try_open_whittler_file_OpensWhittlerFileWithEDITORIfItExists',
'test_write_program_output_to_whittler_file_EmptyStdOutAndStdErr_PrintsErrorAndExits1',
'test_write_program_output_to_whittler_file_ProcessRaisesFileNotFoundError_PrintsErrorAndExits1',
'test_write_program_output_to_whittler_file_NonEmptyStdOutOrStdErr_WritesNonEmptyOneToWhittlerFileAndReturnsItsPath']

class WhittlerProgramTests(unittest.TestCase):

   def setUp(self):
      self.program = Random.string()
      self.command = Random.string()
      self.whittlerFilePath = Random.string()

   def test_make_whittler_filepath_for_command_ReturnsHomeSlashDotWhittlerSlashProgramNameAndArgsDotTxt(self):
      @patch('os.path.expanduser', spec_set=True)
      def testcase(commandArg, expectedExpandUserArgument, _1):
         with self.subTest(f'{commandArg, expectedExpandUserArgument}'):
            expandUserReturnValue = Random.string()
            os.path.expanduser.return_value = expandUserReturnValue
            #
            whittlerFilePath = WhittlerProgram.make_whittler_filepath_for_command(commandArg)
            #
            os.path.expanduser.assert_called_once_with(expectedExpandUserArgument)
            self.assertEqual(expandUserReturnValue, whittlerFilePath)
      testcase('ls', '~/.config/Whittler/ls.txt')
      testcase('systemd --help', '~/.config/Whittler/systemd --help.txt')
      testcase('cmake --help-command set', '~/.config/Whittler/cmake --help-command set.txt')
      testcase('substr /?', '~/.config/Whittler/substr SlashQuestionMark.txt')


   def test_get_module_ReturnsWhittlerProgramModule(self):
      #
      whittlerProgram = WhittlerProgram.get_module()
      #
      self.assertTrue(inspect.ismodule(whittlerProgram))
      self.assertEqual('Whittler.WhittlerProgram', whittlerProgram.__name__)


   @patch('os.environ.get', spec_set=True)
   @patch('Whittler.Process.fail_fast_run', spec_set=True)
   @patch('builtins.print', spec_set=True)
   def test_open_whittler_file_with_editor_environment_variable_OpensFileWithEDITOR(self, printMock, _2, _3):
      editorEnvironmentVariableValue = Random.string()
      os.environ.get.return_value = editorEnvironmentVariableValue
      whittlerFilePath = Random.string()
      #
      WhittlerProgram.open_whittler_file_with_editor_environment_variable(whittlerFilePath)
      #
      self.assertEqual(2, len(printMock.call_args_list))
      printMock.assert_has_calls([
         call('[Whittler] ', end=''),
         call('[Whittler] ExitCode: 0')])
      expectedEditorCommand = f'{editorEnvironmentVariableValue} "{whittlerFilePath}"'
      Process.fail_fast_run.assert_called_once_with(expectedEditorCommand, True)


   def test_prefix_command_with_powershell_dot_exe_if_command_is_get_help_ReturnsPowerShellPrefixedCommandIfGetHelp(self):
      def testcase(command, expectedAdjustedCommand):
         with self.subTest(f'{command, expectedAdjustedCommand}'):
            #
            adjustedCommand = WhittlerProgram.prefix_command_with_powershell_dot_exe_if_command_is_get_help(command)
            #
            self.assertEqual(expectedAdjustedCommand, adjustedCommand)
      testcase('get-help', "powershell.exe -Command 'get-help'")
      testcase('Get-Help', "powershell.exe -Command 'Get-Help'")
      testcase('Get-Help Get-Command -detailed', "powershell.exe -Command 'Get-Help Get-Command -detailed'")
      testcase('whoami', "whoami")
      testcase(' get-help', " get-help")


   @patch('Whittler.WhittlerProgram.open_or_create_whittler_file', spec_set=True)
   def test_run_CallsOpenOrCreateWhittlerFile_Returns0(self, _1):
      command = Random.string()
      #
      exitCode = WhittlerProgram.run(command)
      #
      WhittlerProgram.open_or_create_whittler_file.assert_called_once_with(command)
      self.assertEqual(0, exitCode)


   def test_split_lines_and_remove_leading_and_trailing_whitespace_and_carriage_returns(self):
      def testcase(text, expectedReturnValue):
         with self.subTest(f'{text, expectedReturnValue}'):
            returnValue = WhittlerProgram.split_lines_and_remove_carriage_returns_and_leading_whitespace(text)
            self.assertEqual(expectedReturnValue, returnValue)
      testcase('', [''])
      testcase('abc', ['abc'])
      testcase('\r', [''])
      testcase('\n', ['', ''])
      testcase('\r\n', ['', ''])
      testcase(' \tA\t ', ['A'])
      testcase('\t \t1\t\n2\t\r\n  3 45 ', ['1', '2', '3 45'])
      testcase('\t Line1\r\nLine2\nLine3\r\n\r\nLine4 \t', ['Line1', 'Line2', 'Line3', '', 'Line4'])


   @patch('Whittler.WhittlerProgram.try_open_whittler_file', spec_set=True)
   @patch('Whittler.WhittlerProgram.prefix_command_with_powershell_dot_exe_if_command_is_get_help', spec_set=True)
   @patch('Whittler.WhittlerProgram.write_program_output_to_whittler_file', spec_set=True)
   @patch('Whittler.WhittlerProgram.open_whittler_file_with_editor_environment_variable', spec_set=True)
   def test_open_or_create_whittler_file_WhittlerFileAlreadyExists_OpensItWithEDITOR(self, _1, _2, _3, _4):
      WhittlerProgram.try_open_whittler_file.return_value = True
      powershellAdjustedCommand = Random.string()
      WhittlerProgram.prefix_command_with_powershell_dot_exe_if_command_is_get_help.return_value = powershellAdjustedCommand
      WhittlerProgram.write_program_output_to_whittler_file.return_value = self.whittlerFilePath
      #
      WhittlerProgram.open_or_create_whittler_file(self.command)
      #
      WhittlerProgram.prefix_command_with_powershell_dot_exe_if_command_is_get_help.assert_called_once_with(self.command)
      WhittlerProgram.try_open_whittler_file.assert_called_once_with(powershellAdjustedCommand)
      WhittlerProgram.write_program_output_to_whittler_file.assert_not_called()
      WhittlerProgram.open_whittler_file_with_editor_environment_variable.assert_not_called()


   @patch('Whittler.WhittlerProgram.try_open_whittler_file', spec_set=True)
   @patch('Whittler.WhittlerProgram.prefix_command_with_powershell_dot_exe_if_command_is_get_help', spec_set=True)
   @patch('Whittler.WhittlerProgram.write_program_output_to_whittler_file', spec_set=True)
   @patch('Whittler.WhittlerProgram.open_whittler_file_with_editor_environment_variable', spec_set=True)
   def test_open_or_create_whittler_file_WhittlerFileDoesNotAlreadyExist_CreatesItAndOpensItWithEDITOR(self, _1, _2, _3, _4):
      WhittlerProgram.try_open_whittler_file.return_value = False
      powershellAdjustedCommand = Random.string()
      WhittlerProgram.prefix_command_with_powershell_dot_exe_if_command_is_get_help.return_value = powershellAdjustedCommand
      WhittlerProgram.write_program_output_to_whittler_file.return_value = self.whittlerFilePath
      #
      WhittlerProgram.open_or_create_whittler_file(self.command)
      #
      WhittlerProgram.prefix_command_with_powershell_dot_exe_if_command_is_get_help.assert_called_once_with(self.command)
      WhittlerProgram.try_open_whittler_file.assert_called_once_with(powershellAdjustedCommand)
      WhittlerProgram.write_program_output_to_whittler_file.assert_called_once_with(powershellAdjustedCommand)
      WhittlerProgram.open_whittler_file_with_editor_environment_variable.assert_called_once_with(self.whittlerFilePath)


   def test_try_open_whittler_file_OpensWhittlerFileWithEDITORIfItExists(self):
      @patch('Whittler.WhittlerProgram.make_whittler_filepath_for_command', spec_set=True)
      @patch('os.path.exists', spec_set=True)
      @patch('Whittler.WhittlerProgram.open_whittler_file_with_editor_environment_variable', spec_set=True)
      def testcase(whittlerFilePathExists, expectedReturnValue, _1, _2, _3):
         with self.subTest(f'{whittlerFilePathExists, expectedReturnValue}'):
            makeWhittlerFilePathReturnValue = 'makeWhittlerFilePathReturnValue'
            WhittlerProgram.make_whittler_filepath_for_command.return_value = makeWhittlerFilePathReturnValue
            os.path.exists.return_value = whittlerFilePathExists
            powershellAdjustedCommand = Random.string()
            #
            didOpenWhittlerFile = WhittlerProgram.try_open_whittler_file(powershellAdjustedCommand)
            #
            WhittlerProgram.make_whittler_filepath_for_command.assert_called_once_with(powershellAdjustedCommand)
            os.path.exists.assert_called_once_with(makeWhittlerFilePathReturnValue)
            if whittlerFilePathExists:
               WhittlerProgram.open_whittler_file_with_editor_environment_variable.assert_called_once_with(makeWhittlerFilePathReturnValue)
            else:
               WhittlerProgram.open_whittler_file_with_editor_environment_variable.assert_not_called()
            self.assertEqual(expectedReturnValue, didOpenWhittlerFile)
      testcase(False, False)
      testcase(True, True)


   @patch('Whittler.Process.run', spec_set=True)
   @patch('builtins.print', spec_set=True)
   @patch('sys.exit', spec_set=True)
   def test_write_program_output_to_whittler_file_EmptyStdOutAndStdErr_PrintsErrorAndExits1(self, _1, printMock, _3):
      Process.run.return_value = ('', '')
      #
      WhittlerProgram.write_program_output_to_whittler_file(self.command)
      #
      Process.run.assert_called_once_with(self.command)
      expectedErrorMessage = f"[Whittler] Command '{self.command}' returned empty standard output and empty standard error.\n" +\
         '[Whittler] ExitCode: 1'
      printMock.assert_called_once_with(expectedErrorMessage)
      sys.exit.assert_called_once_with(1)


   @patch('Whittler.Process.run', spec_set=True)
   @patch('builtins.print', spec_set=True)
   @patch('sys.exit', spec_set=True)
   def test_write_program_output_to_whittler_file_ProcessRaisesFileNotFoundError_PrintsErrorAndExits1(self, _1, printMock, _3):
      fileNotFoundError = FileNotFoundError(Random.string())
      Process.run.side_effect = fileNotFoundError
      #
      WhittlerProgram.write_program_output_to_whittler_file(self.command)
      #
      expectedErrorMessage = f"[Whittler] Error: FileNotFoundError raised when running command '{self.command}': " + str(fileNotFoundError) + '\n' +\
         '[Whittler] ExitCode: 1'
      printMock.assert_called_once_with(expectedErrorMessage)
      sys.exit.assert_called_once_with(1)


   def test_write_program_output_to_whittler_file_NonEmptyStdOutOrStdErr_WritesNonEmptyOneToWhittlerFileAndReturnsItsPath(self):
      @patch('Whittler.Process.run', spec_set=True)
      @patch('Whittler.WhittlerProgram.split_lines_and_remove_carriage_returns_and_leading_whitespace', spec_set=True)
      @patch('Whittler.WhittlerProgram.make_whittler_filepath_for_command', spec_set=True)
      @patch('Whittler.File.write_lines', spec_set=True)
      def testcase(stdout, stderr, trueExpectStdoutWrittenFalseExpectStderrWritten, _1, _2, _3, _4):
         with self.subTest(f'{stdout}, {stderr}, {trueExpectStdoutWrittenFalseExpectStderrWritten}'):
            Process.run.return_value = (stdout, stderr)

            whittlerFilePath = Random.string()
            WhittlerProgram.make_whittler_filepath_for_command.return_value = whittlerFilePath

            stdoutOrStderrLinesWithLeadingWhitespaceRemoved = Random.string()
            WhittlerProgram.split_lines_and_remove_carriage_returns_and_leading_whitespace.return_value = stdoutOrStderrLinesWithLeadingWhitespaceRemoved
            #
            returnedWhittlerFilePath = WhittlerProgram.write_program_output_to_whittler_file(self.command)
            #
            Process.run.assert_called_once_with(self.command)
            WhittlerProgram.split_lines_and_remove_carriage_returns_and_leading_whitespace.assert_called_once_with(\
               stdout if trueExpectStdoutWrittenFalseExpectStderrWritten else stderr)
            WhittlerProgram.make_whittler_filepath_for_command.assert_called_once_with(self.command)
            File.write_lines.assert_called_once_with(whittlerFilePath, stdoutOrStderrLinesWithLeadingWhitespaceRemoved)
            self.assertEqual(whittlerFilePath, returnedWhittlerFilePath)
      testcase(Random.string(), '', True)
      testcase('', Random.string(), False)


if __name__ == '__main__': # pragma nocover
   UnitTester.run_tests(WhittlerProgramTests, testNames)
