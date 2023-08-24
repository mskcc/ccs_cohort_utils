#import cohort_utils
from cohort_utils import parsers
#import cohort_utils.parsers

import unittest

COHORTFILE = "./data/COHORT1.cohort.txt"
print(COHORTFILE)

class Hello(unittest.TestCase):
    def say_hi():
       print("hi") 

class TestCRF(unittest.TestCase):
    def test_parse(self):
        parsers.crf.CRF_Handler(crf=COHORTFILE)

if __name__ == "__main__":
    unittest.main()
