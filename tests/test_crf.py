#import cohort_utils
from cohort_utils import parsers
#import cohort_utils.parsers

import unittest

COHORTFILE = "./data/COHORT1.cohort.txt"
print(COHORTFILE)



class TestCRF(unittest.TestCase):
    def test_parse(self):
        crf_handle = parsers.crf.CRF_Handler(crf=COHORTFILE)
        assert len(crf_handle) == 2
        assert crf_handle.meta["projectSubtitle"] == "Project_12345"
        assert crf_handle.cohort_id == "COHORT1"

    def test_tocohort(self):
        crf_handle = parsers.crf.CRF_Handler(crf=COHORTFILE)
        my_cohort = crf_handle.to_cohort()
        assert my_cohort.deliver_somatic
        assert not my_cohort.deliver_germline
        assert len(my_cohort) == 2
        assert my_cohort.cohort_id == "COHORT1"
        assert my_cohort.subtitle == "Project_12345"

    def test_tocrf(self):
        crf_handle = parsers.crf.CRF_Handler(crf=COHORTFILE)
        my_cohort = crf_handle.to_cohort()
        cohort.to_crf()


if __name__ == "__main__":
    unittest.main()
