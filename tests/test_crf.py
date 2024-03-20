import unittest
import cohort_utils

COHORTFILE  = "./data/COHORT1.cohort.txt"
COHORTFILE2 = "./data/COHORT2.cohort.txt"
PAIRINGFILE = "./data/pairing.tsv"

class TestCRF(unittest.TestCase):
    def test_parse(self):
        crf_handle = cohort_utils.parsers.CRF_Handler(crf=COHORTFILE)
        assert len(crf_handle._extract_samples()) == 2
        assert crf_handle._extract_meta() == {'endUsers': ['anoronh4', 'enduser2'], 'pmUsers': ['pmuser1'], 'projectTitle': 'Genomic characterization of Responders', 'projectSubtitle': 'Project_12345'}
        assert crf_handle._extract_cohort_id() == "COHORT1"

    def test_tocohort(self):
        crf_handle = cohort_utils.parsers.CRF_Handler(crf=COHORTFILE)
        my_cohort = crf_handle.to_cohort()
        assert len(my_cohort) == 2
        assert my_cohort.cohort["cohortId"] == "COHORT1"
        assert my_cohort.cohort["projectSubtitle"] == "Project_12345"

    def test_tocrf(self):
        crf_handle = cohort_utils.parsers.CRF_Handler(crf=COHORTFILE)
        my_cohort = crf_handle.to_cohort()
        assert len(my_cohort) == 2
        assert len(my_cohort.cohort["samples"]) == 2
        my_cohort.to_crf()

    def test_add_normals(self):
        pairing = cohort_utils.model.Pairing(file=PAIRINGFILE)
        crf_handle = cohort_utils.parsers.CRF_Handler(crf=COHORTFILE2)
        my_cohort = crf_handle.to_cohort()
        assert len(my_cohort) == 3
        new_cohort = my_cohort.fillin_normals(pairing)
        assert len(new_cohort) == 3

if __name__ == "__main__":
    unittest.main()
