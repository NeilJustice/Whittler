import os
import sys
from typing import List
from Whittler import WhittlerProgram

CommandLineUsage = '''Whittler v0.7.0
https://github.com/NeilJustice/Whittler

Usage: whittler <ProgramName> [ProgramArguments...]

Whittler writes standard output text from a given command line
to file ~/.config/Whittler/<CommandLine>.txt for editing with the EDITOR-defined text editor.
If Whittler has been run previously with the exact same command line arguments,
file ~/.config/Whittler/<CommandLine>.txt is opened with EDITOR for continued editing.
'''

# Example Linux command line arguments:
# systemd --help

# Example Windows command line arguments:
# docker --help

def main(argv: List[str]) -> int:
   if len(argv) < 2 or (len(argv) == 2 and argv[1] == '--help'):
      print(CommandLineUsage)
      return 0
   if not editor_environment_variable_is_defined():
      print('[Whittler] Error: Environment variable EDITOR must be defined with a path to a text editor in order to run Whittler.\n' +\
            '[Whittler] ExitCode: 1')
      return 1
   command = ' '.join(argv[1:])
   whittlerProgram = WhittlerProgram.get_module()
   exitCode: int = whittlerProgram.run(command)
   return exitCode

def editor_environment_variable_is_defined() -> bool:
   editorEnvironmentVariable = os.environ.get('EDITOR')
   return editorEnvironmentVariable is not None

if __name__ == '__main__': # pragma nocover
   sys.exit(main(sys.argv))
