import os, copy, sys, io
import pandas as pd
import json, jsonschema
from cohort_utils import utils
import cohort_utils

class Cohort:
    def __init__(self,**kwargs):
        crj = kwargs.pop("crj",None)
        crj_file = kwargs.pop("crj_file",None)
        if crj:
            self.cohort = crj
        else:
            with open(crj_file, 'r') as f:
                self.cohort = json.load(f)
        self.cohort = utils.clean_nones(self.cohort)
        if "type" not in self.cohort:
            self.cohort["type"] = "investigator"
        if "holdBamsAndFastqs" not in self.cohort:
            self.cohort["holdBamsAndFastqs"] = False
        elif str(self.cohort["holdBamsAndFastqs"]).lower() == "true":
            self.cohort["holdBamsAndFastqs"] = True
        else: self.cohort["holdBamsAndFastqs"] = False
        self.schema = cohort_utils.schema.COHORT_REQUEST_JSON_SCHEMA
        self._validate_schema()

    def __len__(self):
        return len(self.cohort["samples"])

    def to_crf(self):
        crf_string = ""
        crf_string += f"#endUsers:{','.join(self.cohort["endUsers"])}\n"
        crf_string += f"#pmUsers:{','.join(self.cohort["pmUsers"])}\n"
        crf_string += f"#projectTitle:{self.cohort["projectTitle"]}\n"
        if "projectSubtitle" in self.cohort:
            crf_string += f"#projectSubtitle:{self.cohort["projectSubtitle"]}\n"
        crf_string += f"#holdBamsAndFastqs:{self.cohort["holdBamsAndFastqs"]}\n"
        crf_string += "#TUMOR_ID\tNORMAL_ID\tPRIMARY_ID\tNORMAL_PRIMARY_ID\n"
        df = pd.DataFrame(self.cohort["samples"])
        keep_col = "cmoId|normalCmoId|primaryId|normalPrimaryId".split("|")
        for i in keep_col:
            if i not in list(df):
                df[i] = None
        df = df[keep_col]
        s = io.StringIO()
        df.to_csv(s,index=False,header=False,sep="\t")
        crf_string += s.getvalue()
        return crf_string

    def fillin_normals(self,pairing):
        newcohort = copy.deepcopy(self)
        for i in newcohort.cohort["samples"]:
            [t_id,n_id] = pairing.search_tumor(i["cmoId"])
            if n_id != i.get("normalCmoId",None) and not pd.isnull(n_id):
                print(n_id)
                if i.get("normalCmoId",None) == "" or pd.isnull(i.get("normalCmoId",None)):
                    pass
                i["normalCmoId"] = n_id
        return newcohort

    def update_ids(self,metadata_table=None):
        newcohort = copy.deepcopy(self)
        for i in newcohort.cohort["samples"]:
            if i.get("primaryId",None):
                i["cmoId"] = utils.nice_cmo_id(utils.convert_primaryId_to_cmoId(i["primaryId"],metadata_table))
            elif i["cmoId"] and not i.get("primaryId",None):
                i["primaryId"] = utils.convert_cmoId_to_primaryId(i["cmoId"],metadata_table)
            if i.get("normalPrimaryId",None):
                i["normalCmoId"] = utils.nice_cmo_id(utils.convert_primaryId_to_cmoId(i["normalPrimaryId"],metadata_table))
            elif i["normalCmoId"] and not i.get("normalPrimaryId",None):
                i["normalPrimaryId"] = utils.convert_cmoId_to_primaryId(i["normalCmoId"],metadata_table)
        return newcohort

    def _validate_schema(self):
        jsonschema.validators.validate(instance=self.cohort, schema=self.schema)

    def cohort_complete_generate(self,status=None,date=None):
        mod_cohort = copy.deepcopy(self.cohort)
        if "holdBamsAndFastqs" in mod_cohort:
            del mod_cohort["holdBamsAndFastqs"]
        for i in mod_cohort["samples"]:
            if "cmoId" in i:
                del i["cmoId"]
            if "normalCmoId" in i:
                del i["normalCmoId"]
        if status:
            mod_cohort["status"] = status
        if date:
            mod_cohort["date"] = date
        return mod_cohort




