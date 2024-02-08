from cohort_utils import parsers
from cohort_utils.model import Pairing
import unittest
from cohort_utils.parsers.crj import CRJ_Handler
import cohort_utils
import json
#import cohort_utils.schema.CRJ_JSON_SCHEMA as CRJ_JSON_SCHEMA

COHORTFILE  = "./data/COHORT1.cohort.json"

class TestCRJ(unittest.TestCase):
    def test_parse(self):
        with open(COHORTFILE, 'r') as f:
            crj_data = json.load(f)
        crj_handle = parsers.crj.CRJ_Handler(crj_data,cohort_utils.schema.CRJ_JSON_SCHEMA)
        assert len(crj_handle) == 2
        assert crj_handle.crj["meta"]["projectSubtitle"] == "Project_12345"
        assert crj_handle.crj["cohort_id"] == "COHORT1"

    def test_tocohort(self):
        with open(COHORTFILE, 'r') as f:
            crj_data = json.load(f)
        crj_handle = parsers.crj.CRJ_Handler(crj_data,cohort_utils.schema.CRJ_JSON_SCHEMA)
        my_cohort = crj_handle.to_cohort()
        assert my_cohort.deliver_somatic
        assert not my_cohort.deliver_germline
        assert len(my_cohort) == 2
        assert my_cohort.cohort_id == "COHORT1"
        assert my_cohort.subtitle == "Project_12345"

if __name__ == "__main__":
    unittest.main()