from cohort_utils import utils
import pandas as pd
import unittest

class TestUtils(unittest.TestCase):
    def test_categorize_id(self):
        id = "P-0000000-N01-IM0"
        assert utils.categorize_id(id) == "dmpSampleName"

        id = "P-0000000"
        assert utils.categorize_id(id) == "dmpPatientId"

        id = "s_C_XXX000_T001_d03"
        assert utils.categorize_id(id) == "cmoSampleName"
        
        id = "s_C_XXX000_T001_d"
        assert utils.categorize_id(id) == "cmoSampleName"

        id = "C-XXX000-N001-d"
        assert utils.categorize_id(id) == "cmoSampleName"

        id = "07658_AB_1"
        assert utils.categorize_id(id) == "primaryId"

        id = "07658_AB"
        assert utils.categorize_id(id) == "requestId"

    def test_convert_primaryId_to_cmoId(self):
        assert utils.convert_primaryId_to_cmoId("06208_B_21") == "C-000045-M002-d02"
        df = pd.DataFrame({'cmoSampleName': ["Hey"], 'primaryId': ['There']})
        assert utils.convert_primaryId_to_cmoId("There",df) == "Hey"

    def test_convert_cmoId_to_primaryId(self):
        assert utils.convert_cmoId_to_primaryId("C-000045-M002-d02") == "06208_B_21"
        assert utils.convert_cmoId_to_primaryId("s_C_000045_M002_d02") == "06208_B_21"
        df = pd.DataFrame({'cmoSampleName': ["Hey"], 'primaryId': ['There']})
        assert utils.convert_cmoId_to_primaryId("Hey",df) == "There"


if __name__ == "__main__":
    unittest.main()