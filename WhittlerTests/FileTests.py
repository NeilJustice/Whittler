import os
import unittest
from unittest.mock import call, mock_open, patch
from WhittlerTests import Random, UnitTester
from Whittler import File

testNames = ['test_write_lines_CreatesContainingDirectory_WritesFileWithLines']

class FileTests(unittest.TestCase):

   @staticmethod
   @patch('os.path.dirname', spec_set=True)
   @patch('os.makedirs', spec_set=True)
   @patch('builtins.open', spec_set=True)
   def test_write_lines_CreatesContainingDirectory_WritesFileWithLines(openMock, _2, _3):
      filePath = Random.string()
      directoryName = Random.string()
      os.path.dirname.return_value = directoryName
      fileMock = mock_open(openMock)
      line1 = Random.string()
      line2 = Random.string()
      lines = [line1, line2]
      #
      File.write_lines(filePath, lines)
      #
      os.path.dirname.assert_called_once_with(filePath)
      os.makedirs.assert_called_once_with(directoryName, exist_ok=True)
      fileMock.assert_has_calls([
         call(filePath, 'w', encoding='ascii'),
         call().__enter__(),
         call().writelines([line1 + '\n', line2 + '\n']),
         call().__exit__(None, None, None)])

if __name__ == '__main__': # pragma nocover
   UnitTester.run_tests(FileTests, testNames)
