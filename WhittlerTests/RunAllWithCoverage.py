import os
from WhittlerTests import Python

if os.getcwd().endswith('WhittlerTests'):
   os.chdir('..')

Python.run_all_tests_with_coverage(testsProjectName='WhittlerTests', omitPattern='/usr/*,/home/neil/.local/lib/python3.9/site-packages/*')
