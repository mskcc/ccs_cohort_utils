import os,copy,sys
#from .pair import Pair
#from .sample import Sample
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
        if not "type" in self.cohort:
            self.cohort["type"] = "investigator"
        if not "holdBamsAndFastqs" in self.cohort:
            self.cohort["holdBamsAndFastqs"] = False
        print(self.cohort["samples"])
        self.schema = cohort_utils.schema.COHORT_REQUEST_JSON_SCHEMA
        self._validate_schema()

    def __len__(self):
        return len(self.cohort["samples"])

    def to_crf(self,location=sys.stdout):
        print(f"#endUsers:{','.join(self.cohort["endUsers"])}",file=location)
        print(f"#pmUsers:{','.join(self.cohort["pmUsers"])}",file=location)
        print(f"#projectTitle:{self.cohort["projectTitle"]}",file=location)
        print(f"#projectSubtitle:{self.cohort["projectSubtitle"]}",file=location)
        print(f"#holdBamsAndFastqs:{self.cohort["holdBamsAndFastqs"]}",file=location)
        print("#TUMOR_ID\tNORMAL_ID\tPRIMARY_ID\tNORMAL_PRIMARY_ID",file=location)
        df = pd.DataFrame(self.cohort["samples"])
        keep_col = "cmoId|normalCmoId|primaryId|normalPrimaryId".split("|")
        for i in keep_col:
            if i not in list(df):
                df[i] = None
        df = df[keep_col]
        df.to_csv(location,mode='a',index=False,header=False)

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

    def update_ids(self):
        newcohort = copy.deepcopy(self)
        for i in newcohort.cohort["samples"]:
            if i["primaryId"]:
                i["cmoId"] = utils.search_smile_inputid(i["primaryId"]).get("cmoSampleName",None)
            elif i["cmoId"] and not i["primaryId"]:
                i["primaryId"] = utils.search_smile_inputid(i["cmoId"]).get("primaryId",None)
            if i["normalPrimaryId"]:
                i["normalCmoId"] = utils.search_smile_inputid(i["normalPrimaryId"]).get("cmoSampleName",None)
            elif i["normalCmoId"] and not i["normalPrimaryId"]:
                i["normalPrimaryId"] = search_smile_inputid(i["normalCmoId"]).get("primaryId",None)
        return newcohort

    def _validate_schema(self):
        jsonschema.validators.validate(instance=self.cohort, schema=self.schema)
