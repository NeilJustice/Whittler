import threading
from Whittler import Process

class ProcessThread(threading.Thread): # pragma nocover

   def __init__(self, commandIndex: int, command: str, commandSuffixArg: str, outExitCodes: list):
      threading.Thread.__init__(self)
      self.commandIndex = commandIndex
      self.command = command
      self.commandSuffixArg = commandSuffixArg
      self.outExitCodes = outExitCodes

   def run(self) -> None:
      fullCommand = self.command + self.commandSuffixArg
      exitCode = Process.run_and_get_exit_code(fullCommand, False)
      self.outExitCodes[self.commandIndex] = exitCode
