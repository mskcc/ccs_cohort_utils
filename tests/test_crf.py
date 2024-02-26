from cohort_utils import parsers
from cohort_utils.model import Pairing
import unittest
from cohort_utils.parsers.crj import CRJ_Handler
import cohort_utils

COHORTFILE  = "./data/COHORT1.cohort.txt"
COHORTFILE2 = "./data/COHORT2.cohort.txt"
PAIRINGFILE = "./data/pairing.tsv"

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
        my_crj = my_cohort.to_json()
        my_crj_handler = CRJ_Handler(my_crj,cohort_utils.schema.COHORT_REQUEST_JSON_SCHEMA)
        print(my_crj)
        assert len(my_crj_handler) == 2
        assert len(my_crj["manifest"]) == 2

    def test_add_normals(self):
        pairing = Pairing(file=PAIRINGFILE)
        crf_handle = parsers.crf.CRF_Handler(crf=COHORTFILE2)
        my_cohort = crf_handle.to_cohort()
        assert len(my_cohort) == 3
        new_cohort = my_cohort.reconcile_cohort_pairing(pairing)
        assert len(new_cohort) == 3
        assert not my_cohort.is_valid()
        print([i.get_tuple_str() for i in new_cohort.pairs.values()])
        assert new_cohort.is_valid()

if __name__ == "__main__":
    unittest.main()
