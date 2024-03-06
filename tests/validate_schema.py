import json
import jsonschema
import unittest
#from cohort_utils.schema import *
import cohort_utils
import sys

BAM_COMPLETE    = "./data/json/bam-complete.example.json"
MAF_COMPLETE    = "./data/json/maf-complete.example.json"
QC_COMPLETE     = "./data/json/qc-complete.example.json"
COHORT_COMPLETE = "./data/json/cohort-complete.example.json"

class validateschema(unittest.TestCase):
    def test_bam_complete_json(self):
        with open(BAM_COMPLETE,'r') as fh:
            instance = json.load(fh)
        jsonschema.validators.validate(instance=instance, schema=cohort_utils.schema.BAM_COMPLETE_JSON_SCHEMA)
    def test_maf_complete_json(self):
        with open(MAF_COMPLETE,'r') as fh:
            instance = json.load(fh)
        jsonschema.validators.validate(instance=instance, schema=cohort_utils.schema.MAF_COMPLETE_JSON_SCHEMA)
    def test_qc_complete_json(self):
        with open(QC_COMPLETE,'r') as fh:
            instance = json.load(fh)
        jsonschema.validators.validate(instance=instance, schema=cohort_utils.schema.QC_COMPLETE_JSON_SCHEMA)
    def test_cohort_complete_json(self):
        with open(COHORT_COMPLETE,'r') as fh:
            instance = json.load(fh)
        jsonschema.validators.validate(instance=instance, schema=cohort_utils.schema.COHORT_COMPLETE_JSON_SCHEMA)

if __name__ == "__main__":
    unittest.main()