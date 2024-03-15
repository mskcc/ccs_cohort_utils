from cohort_utils import generate_updates
import unittest

MAF  = "./data/mut_somatic.maf"
MAF2 = "./data/mut_somatic_2samples.maf"

class TestSendMessage(unittest.TestCase):
    def test_send_bam_update(self):
        inputs = {"id":"12346_A_1","status":"PASS","date":"2022-10-30 16:05"}
        generate_updates.bam_complete_event(**inputs)

    def test_send_bam_update_invalid(self):
        """
        invalid timestamp
        """
        inputs = {"id":"12346_A_1","status":"PASS","date":"2022-10-3000 16:05"}
        self.assertRaises(Exception, generate_updates.bam_complete_event,**inputs)

    def test_send_maf_update(self):
        generate_updates.cbio_multisample_event(MAF)
    
    def test_send_mixed_maf_update(self):
        generate_updates.cbio_multisample_event(MAF2)




if __name__ == "__main__":
    unittest.main()