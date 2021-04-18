import platform
import shlex
import subprocess
import sys
from typing import Tuple

def append_args(exePath: str, args: str) -> str:
   exePathWithArgs = exePath + (' ' + args if args != '' else '')
   return exePathWithArgs

def fail_fast_run(command: str, runInBackgroundIfWindows: bool) -> None:
   exitCode = run_and_get_exit_code(command, runInBackgroundIfWindows)
   if exitCode != 0:
      singleQuotedCommand = f'\'{command}\''
      print('Command', singleQuotedCommand, 'failed with exit code', exitCode)
      sys.exit(exitCode)

def cross_platform_subprocess_call(command: str, runInBackgroundIfWindows: bool) -> int:
   systemName = platform.system()
   if systemName == 'Windows':
      if runInBackgroundIfWindows:
         subprocess.Popen(command)
         exitCode = 0
      else:
         exitCode = subprocess.call(command)
   else:
      shlexedCommand = shlex.split(command)
      exitCode = subprocess.call(shlexedCommand)
   return exitCode

def run(command: str) -> Tuple[str, str]:
   shlexedCommand = shlex.split(command)
   completedProcess = subprocess.run(shlexedCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
   stdout = completedProcess.stdout.decode('utf-8')
   stderr = completedProcess.stderr.decode('utf-8')
   return (stdout, stderr)

def run_and_get_exit_code(command: str, runInBackgroundIfWindows: bool) -> int:
   singleQuotedCommand = f'\'{command}\''
   print(' Running:', singleQuotedCommand)
   try:
      exitCode = cross_platform_subprocess_call(command, runInBackgroundIfWindows)
   except FileNotFoundError as ex:
      exceptionMessage = str(ex)
      print(exceptionMessage)
      sys.exit(1)
   else:
      return exitCode
