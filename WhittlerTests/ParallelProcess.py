import concurrent.futures
import multiprocessing
import time
from typing import Any
from WhittlerTests import ProcessThread

def run_parallel_processpoolexecutor(func: Any, iterable: Any) -> bool:
   cpuCount = multiprocessing.cpu_count()
   processPoolExecutor = concurrent.futures.ProcessPoolExecutor(cpuCount) # pylint: disable=consider-using-with
   exitCodes = processPoolExecutor.map(func, iterable)
   processPoolExecutor.shutdown(wait=True)
   allCommandsSucceeded = not any(exitCodes)
   return allCommandsSucceeded

def run_parallel_processthread(command: str, commandSuffixArgs: list) -> bool: # pragma nocover
   numberOfCommands = len(commandSuffixArgs)
   processThreads = [None] * numberOfCommands
   processExitCodes = [None] * numberOfCommands
   beginTime = time.process_time()
   for commandIndex, commandSuffixArg in enumerate(commandSuffixArgs):
      processThread = ProcessThread.ProcessThread(commandIndex, command, commandSuffixArg, processExitCodes)
      processThread.start()
      processThreads[commandIndex] = processThread
   for processThread in processThreads:
      processThread.join()
   endTime = time.process_time()
   elapsedMilliseconds = int((endTime - beginTime) * 1000)
   allProcessesExitedZero = not any(processExitCodes)
   print('Done in', elapsedMilliseconds, 'ms')
   print('All processes exited 0:', allProcessesExitedZero)
   return allProcessesExitedZero
