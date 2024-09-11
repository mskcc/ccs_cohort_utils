import unittest
import cohort_utils
import json,jsonschema
import pandas as pd
import tempfile
import os
import logging
logging.basicConfig(level=logging.DEBUG)
from utils import run_test


class TestSample(unittest.TestCase):
    @run_test
    def test_sample(self):
        metadata_table = pd.DataFrame(
            {
                'cmoSampleName': ["s_C_AAAAAA_P001_d","s_C_BBBBBB_P001_d","s_C_AAAAAA_N001_d","s_C_BBBBBB_N001_d"],
                'primaryId': ['78787_AB_1','78787_1','95959_8','96785_G_4']
            }
        )
        a_sample = cohort_utils.model.Sample(**{"cmoId":"s_C_XXXXXX_N001_d","primaryId":"12345_3"})
        b_sample = cohort_utils.model.Sample(**{"cmoId":"s_C_AAAAAA_P001_d"})
        b_sample.update_sample_with_metadata(metadata_table)
        assert b_sample.metadata["primaryId"] == "78787_AB_1"
        c_sample = cohort_utils.model.Sample(**{"primaryId":"95959_8"})
        c_sample.update_sample_with_metadata(metadata_table)
        assert c_sample.metadata["cmoId"] == "s_C_AAAAAA_N001_d"
        d_sample = cohort_utils.model.Sample(**{"primaryId":"12345_3"})
        #d_sample.update_sample_with_metadata(metadata_table)
        self.assertRaises(IndexError, d_sample.update_sample_with_metadata,metadata_table)
        e_sample = cohort_utils.model.Sample(**{"primaryId":"95959_8"})
        self.assertRaises(KeyError, e_sample.update_sample_with_smile)
        f_sample = cohort_utils.model.Sample(**{"primaryId":"15300_12"})
        f_sample.update_sample_with_smile()
        assert f_sample.metadata["cmoId"] == "s_C_H5E30A_M005_d05"



if __name__ == "__main__":
    unittest.main()
