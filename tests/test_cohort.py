from cohort_utils import parsers
from cohort_utils.model import Pairing
import unittest
from cohort_utils.parsers.crj import CRJ_Handler
import cohort_utils
import json
#import cohort_utils.schema.CRJ_JSON_SCHEMA as CRJ_JSON_SCHEMA

COHORTFILE  = "./data/json/cohort-complete.example.json"

class TestCRJ(unittest.TestCase):
    def test_crj_obj(self):
        with open(COHORTFILE, 'r') as f:
            crj_data = json.load(f)
        mycohort = cohort_utils.model.Cohort(crj = crj_data)
        assert len(mycohort) == 3
        assert mycohort.cohort["projectSubtitle"] == "A longer description"
        assert mycohort.cohort["cohortId"] == "CCS_PPPQQQQ"

if __name__ == "__main__":
    unittest.main()