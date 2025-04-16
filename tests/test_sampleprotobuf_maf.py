import unittest
from utils import run_test
from cohort_utils.sampleprotobuf_tempoMaf import SampleProtobuf_Handler

MAF  = "./data/mut_somatic.maf"

class TestProtobuf(unittest.TestCase):
    @run_test
    def test_sampleprotobuf(self):
        sph = SampleProtobuf_Handler(maf=MAF)
        tm = sph.generate_tempomessage()
        print(tm)

if __name__ == "__main__":
    unittest.main()
