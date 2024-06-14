import unittest
import cohort_utils
from utils import run_test

VOYAGER1  = "./data/voyager1/"
VOYAGER2  = "./data/voyager2/"

class TestVoyager(unittest.TestCase):
    @run_test
    def test_voyager_compare(self):
        voyager1 = cohort_utils.model.VoyagerTempoMPGen(folderPath = VOYAGER1)
        voyager2 = cohort_utils.model.VoyagerTempoMPGen(folderPath = VOYAGER2)
        compare_result = voyager1.compare(voyager2)
        print(compare_result[["primaryId","CMO_Sample_ID_new","CMO_Sample_ID_old","dropped","added","bait_change"]])

if __name__ == "__main__":
    unittest.main()