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
        cohort_utils.model.VoyagerTempoMPGen(folderPath=VOYAGER1)

    def test_missing_required_column_raises(self):
        tmpdir = self._make_temp_voyager({
            "sample_tracker.txt": "CMO_Sample_ID\nA_T\nB_T\n"
        })
        with self.assertRaises(ValueError) as ctx:
            cohort_utils.model.VoyagerTempoMPGen(folderPath=tmpdir)
        self.assertIn("tracker", str(ctx.exception))
        self.assertIn("primaryId", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
