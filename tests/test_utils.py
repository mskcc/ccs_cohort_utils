import cohort_utils
import pandas as pd
import unittest
from utils import run_test

class TestUtils(unittest.TestCase):
    @run_test
    def test_categorize_id(self):
        id = "P-0000000-N01-IM0"
        assert cohort_utils.utils.categorize_id(id) == "dmpSampleName"

        id = "P-0000000"
        assert cohort_utils.utils.categorize_id(id) == "dmpPatientId"

        id = "s_C_XXX000_T001_d03"
        assert cohort_utils.utils.categorize_id(id) == "cmoSampleName"

        id = "s_C_XXX000_T001_d"
        assert cohort_utils.utils.categorize_id(id) == "cmoSampleName"

        id = "C-XXX000-N001-d"
        assert cohort_utils.utils.categorize_id(id) == "cmoSampleName"

        id = "07658_AB_1"
        assert cohort_utils.utils.categorize_id(id) == "primaryId"

        id = "07658_C_1"
        assert cohort_utils.utils.categorize_id(id) == "primaryId"

        id = "07658_AB"
        assert cohort_utils.utils.categorize_id(id) == "requestId"

    @run_test
    def test_convert_primaryId_to_cmoId(self):
        assert cohort_utils.utils.convert_primaryId_to_cmoId("06208_B_21") == "C-000045-T004-d"
        df = pd.DataFrame({'cmoSampleName': ["Hey"], 'primaryId': ['There']})
        assert cohort_utils.utils.convert_primaryId_to_cmoId("There",df) == "Hey"

    @run_test
    def test_convert_cmoId_to_primaryId(self):
        assert cohort_utils.utils.convert_cmoId_to_primaryId("C-000045-T004-d") == "06208_B_21"
        assert cohort_utils.utils.convert_cmoId_to_primaryId("s_C_000045_T004_d") == "06208_B_21"
        df = pd.DataFrame({'cmoSampleName': ["Hey"], 'primaryId': ['There']})
        assert cohort_utils.utils.convert_cmoId_to_primaryId("Hey",df) == "There"

if __name__ == "__main__":
    unittest.main()
