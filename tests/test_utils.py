from cohort_utils import utils
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


if __name__ == "__main__":
    unittest.main()