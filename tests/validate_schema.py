import json
import jsonschema
import unittest
import cohort_utils
import sys
from utils import run_test

BAM_COMPLETE    = "./data/json/bam-complete.example.json"
MAF_COMPLETE    = "./data/json/maf-complete.example.json"
QC_COMPLETE     = "./data/json/qc-complete.example.json"
COHORT_COMPLETE = "./data/json/cohort-complete.example.json"
COHORT_REQUEST  = "./data/json/COHORT1.cohort.json"

class validateschema(unittest.TestCase):
    @run_test
    def test_bam_complete_json(self):
        with open(BAM_COMPLETE,'r') as fh:
            instance = json.load(fh)
        jsonschema.validators.validate(instance=instance, schema=cohort_utils.schema.BAM_COMPLETE_JSON_SCHEMA)
        instance_bad = {k:instance[k] for k in instance if k != "primaryId"}
        self.assertRaises(Exception,jsonschema.validators.validate,instance=instance_bad, schema=cohort_utils.schema.BAM_COMPLETE_JSON_SCHEMA)
        instance_2 = {**instance_bad,"cmoId":"s_C_XXXXXX_P001_d"}
        jsonschema.validators.validate(instance=instance_2, schema=cohort_utils.schema.BAM_COMPLETE_JSON_SCHEMA)
        instance_3 = {**instance,"cmoId":"s_C_XXXXXX_P001_d"}
        jsonschema.validators.validate(instance=instance_3, schema=cohort_utils.schema.BAM_COMPLETE_JSON_SCHEMA)
    @run_test
    def test_maf_complete_json(self):
        with open(MAF_COMPLETE,'r') as fh:
            instance = json.load(fh)
        jsonschema.validators.validate(instance=instance, schema=cohort_utils.schema.MAF_COMPLETE_JSON_SCHEMA)
    @run_test
    def test_qc_complete_json(self):
        with open(QC_COMPLETE,'r') as fh:
            instance = json.load(fh)
        jsonschema.validators.validate(instance=instance, schema=cohort_utils.schema.QC_COMPLETE_JSON_SCHEMA)
    @run_test
    def test_cohort_complete_json(self):
        with open(COHORT_COMPLETE,'r') as fh:
            instance = json.load(fh)
        jsonschema.validators.validate(instance=instance, schema=cohort_utils.schema.COHORT_COMPLETE_JSON_SCHEMA)
    @run_test
    def test_cohort_request_json(self):
        with open(COHORT_REQUEST,'r') as fh:
            instance = json.load(fh)
        jsonschema.validators.validate(instance=instance, schema=cohort_utils.schema.COHORT_REQUEST_JSON_SCHEMA)

if __name__ == "__main__":
    unittest.main()