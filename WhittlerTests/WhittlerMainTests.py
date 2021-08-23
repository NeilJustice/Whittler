import os
import unittest
from unittest.mock import Mock, patch
from Whittler import WhittlerMain, WhittlerProgram
from WhittlerTests import Random, UnitTester

testNames = [
'test_main_0Or1Arg_WritesCommandLineUsageAndReturns0',
'test_main_FirstArgIsDashDashHelp_PrintsCommandLineUsage_ExitsWithCode0',
'test_main_TwoOrMoreArgs_EDITORIsNotDefined_PrintsErrorMessage_ExitsWithCode1',
'test_main_TwoOrMoreArgs_EDITORIsDefined_CallsWhittlerProgramRun_ExitsWithRunReturnValue',
'test_editor_environment_variable_is_defined_ReturnsTrueIfEDITOREnvironmentVariableDefined'
]

class WhittlerMainTests(unittest.TestCase):

   ExpectedCommandLineUsage = '''Whittler v0.7.0 - Facilitates whittling away (deleting) "inessential" standard output text.

Usage: whittler <ProgramName> [ProgramArguments...]

Whittler writes standard output text from a given command line
to file ~/.config/Whittler/<CommandLine>.txt for editing with the EDITOR-defined text editor.
If Whittler has been run previously with the exact same command line arguments,
file ~/.config/Whittler/<CommandLine>.txt is opened with EDITOR for continued whittling/editing.
'''

   def setUp(self):
      self.programName = Random.string()
      self.programArgument1 = Random.string()
      self.programArgument2 = Random.string()
      self.whittlerFilePath = Random.string()

   def test_main_0Or1Arg_WritesCommandLineUsageAndReturns0(self):
      @patch('builtins.print', spec_set=True)
      def testcase(argvLength, printMock):
         with self.subTest(f'{argvLength}'):
            #
            exitCode = WhittlerMain.main([0] * argvLength)
            #
            printMock.assert_called_once_with(self.ExpectedCommandLineUsage)
            self.assertEqual(0, exitCode)
      testcase(0)
      testcase(1)

   @patch('builtins.print', spec_set=True)
   def test_main_FirstArgIsDashDashHelp_PrintsCommandLineUsage_ExitsWithCode0(self, printMock):
      #
      exitCode = WhittlerMain.main(['Whittler.py', '--help'])
      #
      printMock.assert_called_once_with(self.ExpectedCommandLineUsage)
      self.assertEqual(0, exitCode)

   def test_main_TwoOrMoreArgs_EDITORIsNotDefined_PrintsErrorMessage_ExitsWithCode1(self):
      @patch('Whittler.WhittlerMain.editor_environment_variable_is_defined', spec_set=True)
      @patch('builtins.print', spec_set=True)
      def testcase(argv, printMock, _2):
         with self.subTest(f'{argv}'):
            WhittlerMain.editor_environment_variable_is_defined.return_value = False
            #
            returnValue = WhittlerMain.main(argv)
            #
            WhittlerMain.editor_environment_variable_is_defined.assert_called_once_with()
            printMock.assert_called_once_with(
               '[Whittler] Error: Environment variable EDITOR must be defined with a path to a text editor in order to run Whittler.\n' +\
               '[Whittler] ExitCode: 1')
            self.assertEqual(1, returnValue)
      testcase([Random.string(), self.programName])
      testcase([Random.string(), self.programName, 'arg1'])

   def test_main_TwoOrMoreArgs_EDITORIsDefined_CallsWhittlerProgramRun_ExitsWithRunReturnValue(self):
      @patch('Whittler.WhittlerMain.editor_environment_variable_is_defined', spec_set=True)
      @patch('Whittler.WhittlerProgram.get_module', spec_set=True)
      def testcase(argv, expectedCommand, _1, _2):
         with self.subTest(f'{argv, expectedCommand}'):
            WhittlerMain.editor_environment_variable_is_defined.return_value = True

            whittlerProgramMock = Mock()
            runReturnValue = Random.integer()
            whittlerProgramMock.run.return_value = runReturnValue
            WhittlerProgram.get_module.return_value = whittlerProgramMock
            #
            exitCode = WhittlerMain.main(argv)
            #
            WhittlerMain.editor_environment_variable_is_defined.assert_called_once_with()
            WhittlerProgram.get_module.assert_called_once_with()
            whittlerProgramMock.run.assert_called_once_with(expectedCommand)
            self.assertEqual(runReturnValue, exitCode)
      testcase(['Whittler.py', self.programName], f'{self.programName}')
      testcase(['Whittler.py', self.programName, self.programArgument1], f'{self.programName} {self.programArgument1}')
      testcase(['Whittler.py', self.programName, self.programArgument1, self.programArgument2], f'{self.programName} {self.programArgument1} {self.programArgument2}')

   def test_editor_environment_variable_is_defined_ReturnsTrueIfEDITOREnvironmentVariableDefined(self):
      @patch('os.environ.get', spec_set=True)
      def testcase(expectedReturnValue, editorValue, _1):
         with self.subTest(f'{expectedReturnValue, editorValue}'):
            os.environ.get.return_value = editorValue
            #
            editorDefined = WhittlerMain.editor_environment_variable_is_defined()
            #
            os.environ.get.assert_called_once_with('EDITOR')
            self.assertEqual(expectedReturnValue, editorDefined)
      testcase(True, '/usr/bin/vim')
      testcase(True, '')
      testcase(False, None)

if __name__ == '__main__': # pragma nocover
   UnitTester.run_tests(WhittlerMainTests, testNames)
