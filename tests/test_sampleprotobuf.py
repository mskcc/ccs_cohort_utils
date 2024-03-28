import unittest
import cohort_utils

MAF  = "./data/mut_somatic.maf"

class TestProtobuf(unittest.TestCase):
    def test_sampleprotobuf(self):
        sph = cohort_utils.sampleprotobuf.SampleProtobuf_Handler(maf=MAF)
        tm = sph.generate_tempomessage()
        print(tm)

if __name__ == "__main__":
    unittest.main()