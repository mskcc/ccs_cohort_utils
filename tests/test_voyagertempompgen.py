import unittest
import os
import shutil
import tempfile
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


class TestVoyagerValidation(unittest.TestCase):
    def _make_temp_voyager(self, overrides):
        """Copy voyager1 data into a fresh temp dir, overriding specified files."""
        tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmpdir)
        for fname in os.listdir(VOYAGER1):
            shutil.copy(os.path.join(VOYAGER1, fname), os.path.join(tmpdir, fname))
        for fname, content in overrides.items():
            with open(os.path.join(tmpdir, fname), 'w') as f:
                f.write(content)
        return tmpdir

    def test_valid_data_passes(self):
        v = cohort_utils.model.VoyagerTempoMPGen(folderPath=VOYAGER1)
        self.assertIsNotNone(v)

    def test_missing_required_column_raises(self):
        tmpdir = self._make_temp_voyager({
            "sample_tracker.txt": "CMO_Sample_ID\nA_T\nB_T\n"
        })
        with self.assertRaises(ValueError) as ctx:
            cohort_utils.model.VoyagerTempoMPGen(folderPath=tmpdir)
        self.assertIn("tracker", str(ctx.exception))
        self.assertIn("primaryId", str(ctx.exception))

    def test_pairing_tumor_not_in_tracker_raises(self):
        tmpdir = self._make_temp_voyager({
            "sample_pairing.txt": "TUMOR_ID\tNORMAL_ID\nA_T\tA_N\nUNKNOWN_T\tA_N\n"
        })
        with self.assertRaises(ValueError) as ctx:
            cohort_utils.model.VoyagerTempoMPGen(folderPath=tmpdir)
        self.assertIn("pairing", str(ctx.exception))
        self.assertIn("UNKNOWN_T", str(ctx.exception))

    def test_pairing_normal_not_in_tracker_raises(self):
        tmpdir = self._make_temp_voyager({
            "sample_pairing.txt": "TUMOR_ID\tNORMAL_ID\nA_T\tA_N\nB_T\tUNKNOWN_N\n"
        })
        with self.assertRaises(ValueError) as ctx:
            cohort_utils.model.VoyagerTempoMPGen(folderPath=tmpdir)
        self.assertIn("pairing", str(ctx.exception))
        self.assertIn("UNKNOWN_N", str(ctx.exception))

    def test_mapping_sample_not_in_tracker_raises(self):
        tmpdir = self._make_temp_voyager({
            "sample_mapping.txt": "SAMPLE\tTARGET\tFASTQ_PE1\tFASTQ_PE2\nA_T\tidt\t/p/1.fastq.gz\t/p/2.fastq.gz\nUNKNOWN_S\tidt\t/p/3.fastq.gz\t/p/4.fastq.gz\n"
        })
        with self.assertRaises(ValueError) as ctx:
            cohort_utils.model.VoyagerTempoMPGen(folderPath=tmpdir)
        self.assertIn("mapping", str(ctx.exception))
        self.assertIn("UNKNOWN_S", str(ctx.exception))

    def test_conflict_citag_not_in_tracker_raises(self):
        tmpdir = self._make_temp_voyager({
            "sample_conflict.txt": "ciTag\tcmoPatientId\tprimaryId\tsampleClass\trunMode\tsampleType\tbaitSet\trunDate\tConflict Reason\nUNKNOWN_C\tC-AAA\t12345_1\tTumor\tWES\tDNA\tidt\t2024-01-01\treason\n"
        })
        with self.assertRaises(ValueError) as ctx:
            cohort_utils.model.VoyagerTempoMPGen(folderPath=tmpdir)
        self.assertIn("conflict", str(ctx.exception))
        self.assertIn("UNKNOWN_C", str(ctx.exception))

    def test_unpaired_citag_not_in_tracker_raises(self):
        tmpdir = self._make_temp_voyager({
            "sample_unpaired.txt": "ciTag\tcmoPatientId\tprimaryId\tsampleClass\trunMode\tsampleType\tbaitSet\trunDate\tPossible Reason?\nUNKNOWN_U\tC-AAA\t12345_1\tTumor\tWES\tDNA\tidt\t2024-01-01\treason\n"
        })
        with self.assertRaises(ValueError) as ctx:
            cohort_utils.model.VoyagerTempoMPGen(folderPath=tmpdir)
        self.assertIn("unpaired", str(ctx.exception))
        self.assertIn("UNKNOWN_U", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
