import os
import sys
from typing import Any, List
from Whittler import File, Process

def make_whittler_filepath_for_command(command: str) -> str:
   commandWithSlashAndQuestionMarkReplaced = command.replace('/', 'Slash').replace('?', 'QuestionMark')
   whittlerFilePath = os.path.expanduser(f'~/.config/Whittler/{commandWithSlashAndQuestionMarkReplaced}.txt')
   return whittlerFilePath

def open_or_create_whittler_file(command: str) -> None:
   powershellAdjustedCommand = prefix_command_with_powershell_dot_exe_if_command_is_get_help(command)
   if try_open_whittler_file(powershellAdjustedCommand):
      return
   whittlerFilePath = write_program_output_to_whittler_file(powershellAdjustedCommand)
   open_whittler_file_with_editor_environment_variable(whittlerFilePath)

def open_whittler_file_with_editor_environment_variable(whittlerFilePath: str) -> None:
   editorEnvironmentVariableValue = os.environ.get('EDITOR')
   editorCommand = f'{editorEnvironmentVariableValue} "{whittlerFilePath}"'
   print('[Whittler] ', end='')
   Process.fail_fast_run(editorCommand, True)
   print('[Whittler] ExitCode: 0')

def prefix_command_with_powershell_dot_exe_if_command_is_get_help(command: str) -> str:
   casefoldedCommand = command.casefold()
   if casefoldedCommand.startswith('get-help'):
      return f"powershell.exe -Command '{command}'"
   return command

def run(command: str) -> int:
   open_or_create_whittler_file(command)
   return 0

def split_lines_and_remove_carriage_returns_and_leading_whitespace(text: str) -> List[str]:
   textWithCarriageReturnsRemoved = text.replace('\r', '')
   lines = textWithCarriageReturnsRemoved.split('\n')
   linesWithLeadingWhiteSpaceRemoved = map(str.lstrip, lines)
   linesWithLeadingAndTrailingWhiteSpaceRemoved = list(map(str.rstrip, linesWithLeadingWhiteSpaceRemoved))
   return linesWithLeadingAndTrailingWhiteSpaceRemoved

def try_open_whittler_file(powershellAdjustedCommand: str) -> bool:
   whittlerFilePath = make_whittler_filepath_for_command(powershellAdjustedCommand)
   if os.path.exists(whittlerFilePath):
      open_whittler_file_with_editor_environment_variable(whittlerFilePath)
      return True
   return False

def write_program_output_to_whittler_file(command: str) -> str:
   try:
      (stdout, stderr) = Process.run(command)
      textToWriteToWhittlerFile = ''
      if stdout != '':
         textToWriteToWhittlerFile = stdout
      elif stderr != '':
         textToWriteToWhittlerFile = stderr
      else:
         errorMessage = f"[Whittler] Command '{command}' returned empty standard output and empty standard error.\n" +\
            '[Whittler] ExitCode: 1'
         print(errorMessage)
         sys.exit(1)
      stdoutOrStderrLinesWithLeadingWhitespaceRemoved =\
         split_lines_and_remove_carriage_returns_and_leading_whitespace(textToWriteToWhittlerFile)
      whittlerFilePath = make_whittler_filepath_for_command(command)
      File.write_lines(whittlerFilePath, stdoutOrStderrLinesWithLeadingWhitespaceRemoved)
      return whittlerFilePath
   except FileNotFoundError as ex:
      errorMessage = f"[Whittler] Error: FileNotFoundError raised when running command '{command}': " + str(ex) + '\n' +\
         '[Whittler] ExitCode: 1'
      print(errorMessage)
      sys.exit(1)

def get_module() -> Any:
   whittlerProgramModule = __import__(__name__).WhittlerProgram
   return whittlerProgramModule
