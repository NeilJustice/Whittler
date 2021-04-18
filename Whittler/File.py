from typing import List
import os

def write_lines(filePath: str, lines: List[str]) -> None:
   directoryName = os.path.dirname(filePath)
   os.makedirs(directoryName, exist_ok=True)
   with open(filePath, 'w') as file:
      linesWithNewlineEndings = list(map(lambda line: line + '\n', lines))
      file.writelines(linesWithNewlineEndings)
