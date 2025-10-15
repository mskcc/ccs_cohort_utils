import unittest
import cohort_utils
import json,jsonschema
import pandas as pd
import tempfile
import os
import logging
logging.basicConfig(level=logging.DEBUG)
from utils import run_test

COHORT_COMPLETE_JSON  = "./data/json/cohort-complete.example.json"
COHORT_REQUEST_JSON   = "./data/json/COHORT1.cohort.json"
COHORT_REQUEST_JSON2  = "./data/json/COHORT2.cohort.json"
COHORT_REQUEST_JSON3  = "./data/json/COHORT3.cohort.json"

class TestCRJ(unittest.TestCase):
    @run_test
    def test_crj_obj(self):
        with open(COHORT_REQUEST_JSON, 'r') as f:
            crj_data = json.load(f)
        mycohort = cohort_utils.model.Cohort(crj = crj_data)
        assert len(mycohort) == 2
        assert mycohort.cohort["projectSubtitle"] == "Project_12345"
        assert mycohort.cohort["cohortId"] == "COHORT1"

    @run_test
    def test_cohort_update_ids(self):
        with open(COHORT_REQUEST_JSON, 'r') as f:
            crj_data = json.load(f)
        mycohort = cohort_utils.model.Cohort(crj = crj_data)
        assert len(mycohort) == 2
        metadata_table = pd.DataFrame(
            {
                'cmoSampleName': ["s_C_AAAAAA_P001_d","s_C_BBBBBB_P001_d","s_C_AAAAAA_N001_d","s_C_BBBBBB_N001_d"],
                'primaryId': ['78787_AB_1','78787_1','95959_8','96785_G_4']
            }
        )
        #newcohort = mycohort.update_ids(metadata_table)
        newcohort = mycohort.update_with_metadata_table(metadata_table)
        assert newcohort.cohort['samples'][0]['primaryId'] == '78787_AB_1'
        assert newcohort.cohort['samples'][0]['normalPrimaryId'] == '95959_8'
        assert newcohort.cohort['samples'][1]['cmoId'] == 's_C_BBBBBB_P001_d'

        with open(COHORT_REQUEST_JSON3, 'r') as f:
            crj_data = json.load(f)
        mycohort = cohort_utils.model.Cohort(crj = crj_data)
        newcohort = mycohort.update_with_smile()
        assert newcohort.cohort['samples'][0] == {'cmoId': 's_C_H5E30A_M005_d05', 'normalCmoId': 's_C_H5E30A_N003_d03', 'primaryId': '15300_12', 'oncotreeCode': 'NSCLC', 'normalPrimaryId': '15300_13'}
        cohort_complete_json = newcohort.cohort_complete_generate(use_cmoid=True)
        assert cohort_complete_json['samples'] == [{'cmoId': 'C-H5E30A-M005-d05', 'normalCmoId': 'C-H5E30A-N003-d03'}]

        newcohort = mycohort.update_with_smile(overwrite=True,additional_required_fields=["investigatorSampleId","oncotreeCode"])
        assert newcohort.cohort['samples'][0] == {'cmoId': 's_C_H5E30A_M005_d05', 'normalCmoId': 's_C_H5E30A_N003_d03', 'primaryId': '15300_12', 'investigatorSampleId': 'P-0058090-T02-WES', 'oncotreeCode': 'NSCLC', 'normalPrimaryId': '15300_13', 'normalInvestigatorSampleId': 'P-0058090-N02-WES'}

    @run_test
    def test_cohort_addnormals(self):
        with open(COHORT_REQUEST_JSON2, 'r') as f:
            crj_data = json.load(f)
        mycohort = cohort_utils.model.Cohort(crj = crj_data)
        assert len(mycohort) == 2
        pairing_table = pd.DataFrame(
            {
                'TUMOR_ID':['s_C_AAAAAA_P001_d','s_C_BBBBBB_P001_d'],
                'NORMAL_ID':['s_C_AAAAAA_N001_d','s_C_BBBBBB_N001_d']
            }
        )
        with tempfile.NamedTemporaryFile(mode='w+t', suffix='.csv',delete=False) as f:
            pairing_table.to_csv(f,index=False,sep="\t")
            pairing_file = f.name
        pairing_obj = cohort_utils.model.Pairing(file = pairing_file)
        os.remove(pairing_file)
        newcohort = mycohort.fillin_normals(pairing_obj)
        jsonschema.validators.validate(instance=newcohort.cohort, schema=cohort_utils.schema.COHORT_REQUEST_JSON_SCHEMA)
        metadata_table = pd.DataFrame(
            {
                'cmoSampleName': ["s_C_AAAAAA_P001_d","s_C_BBBBBB_P001_d","s_C_AAAAAA_N001_d","s_C_BBBBBB_N001_d"],
                'primaryId': ['78787_AB_1','78787_1','95959_8','96785_G_4']
            }
        )
        #newercohort = newcohort.update_ids(metadata_table)
        newercohort = newcohort.update_with_metadata_table(metadata_table)
        jsonschema.validators.validate(instance=newercohort.cohort, schema=cohort_utils.schema.COHORT_REQUEST_JSON_SCHEMA)
        x = newercohort.cohort_complete_generate(date="2022-11-12 21:59",status="PASS")
        # keep the following assertion to make sure cohort_complete_generate doesn't modify the original object.
        jsonschema.validators.validate(instance=newercohort.cohort_complete_generate(date="2022-11-12 21:59",status="PASS",pipelineVersion="v2"), schema=cohort_utils.schema.COHORT_COMPLETE_JSON_SCHEMA)

if __name__ == "__main__":
    unittest.main()
