#import os
import copy
#import sys
import io
import pandas as pd
import numpy as np
import json
import jsonschema
from cohort_utils import utils
import cohort_utils
from .voyager_tracker import VoyagerTempoMPGen
import logging
logger = logging.getLogger(__name__)

class Cohort:
    def __init__(self,**kwargs):
        crj = kwargs.pop("crj",None)
        crj_file = kwargs.pop("crj_file",None)
        if crj:
            self.cohort = crj
        else:
            with open(crj_file, 'r') as f:
                self.cohort = json.load(f)
        logger.debug('Ingesting cohortId: {}'.format(self.cohort["cohortId"]))
        self.cohort = utils.clean_nones(self.cohort)
        if "type" not in self.cohort:
            self.cohort["type"] = "investigator"
        if "deliverBam" not in self.cohort:
            self.cohort["deliverBam"] = True
        if "deliverFastq" not in self.cohort:
            self.cohort["deliverFastq"] = False
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
        crf_string += f"#deliverBam:{self.cohort["deliverBam"]}\n"
        crf_string += f"#deliverFastq:{self.cohort["deliverFastq"]}\n"
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
                try:
                    i["cmoId"] = utils.nice_cmo_id(utils.convert_primaryId_to_cmoId(i["primaryId"],metadata_table))
                except Exception as e:
                    pass
            elif i["cmoId"] and not i.get("primaryId",None):
                try:
                    i["primaryId"] = utils.convert_cmoId_to_primaryId(i["cmoId"],metadata_table)
                except Exception as e:
                    pass
            if i.get("normalPrimaryId",None):
                try:
                    i["normalCmoId"] = utils.nice_cmo_id(utils.convert_primaryId_to_cmoId(i["normalPrimaryId"],metadata_table))
                except Exception as e:
                    pass
            elif i["normalCmoId"] and not i.get("normalPrimaryId",None):
                try:
                    i["normalPrimaryId"] = utils.convert_cmoId_to_primaryId(i["normalCmoId"],metadata_table)
                except Exception as e:
                    pass
        return newcohort

    def _validate_schema(self,schema=None):
        if not schema:
            schema = self.schema
        jsonschema.validators.validate(instance=self.cohort, schema=schema)

    def cohort_complete_generate(self,status=None,date=None):
        mod_cohort = copy.deepcopy(self.cohort)
        if "deliverBam" in mod_cohort:
            del mod_cohort["deliverBam"]
        if "deliverFastq" in mod_cohort:
            del mod_cohort["deliverFastq"]
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

    def generate_missing_table(self):
        """
        identify tumors that are missing normalCmoId, primaryId, or normalPrimaryId
        assume update_ids and fillin_normals has been run.
        """
        pair_table = pd.DataFrame(self.cohort["samples"])
        if "primaryId" not in list(pair_table):
            pair_table["primaryId"] = np.nan
        if "normalPrimaryId" not in list(pair_table):
            pair_table["primaryId"] = np.nan
        missing_pair_table = pair_table[pair_table.isnull().any(axis=1)]
        return missing_pair_table

    def get_sample_list(self,sampleType="all",idType="cmo",dedup=False):
        """
        idType should be cmo or primary
        sampleType should be tumor, normal or all
        gets the names of all samples in the cohort
        """
        if idType == "cmo":
            tumors = [i["cmoId"] for i in self.cohort["samples"]]
            normals = [i["normalCmoId"] for i in self.cohort["samples"]]
        elif idType == "primary":
            tumors = [i["primaryId"] for i in self.cohort["samples"]]
            normals = [i["normalPrimaryId"] for i in self.cohort["samples"]]
        else:
            raise TypeError("wrong idType; should be either cmo or primary")
        if sampleType == "all":
            sampleList = tumors + normals
        elif sampleType =="tumor":
            sampleList = tumors
        elif sampleType =="normal":
            sampleList = normals
        else:
            raise TypeError("wrong sampleType; should be all, tumor or normal")
        if dedup:
            return list(set(sampleList))
        else:
            return sampleList

    def get_pair_list(self,idType="cmo"):
        """
        idType should be cmo or primary
        gets the names of all samples and returns them as a list of tuples,
        where each tuple contains the tumor and the normal
        ex: [(tumor1,normal1),(tumor2,normal2)]
        """
        tumors = self.get_sample_list(sampleType="tumors",idType=idType,dedup=False)
        normals = self.get_sample_list(sampleType="normals",idType=idType,dedup=False)
        return list(zip(tumors, normals))

    def generate_voyager_conflicts_table(self,voyager_obj,filter_col=None):
        """
        Filter the voyager conflicts table
        """
        all_samples = self.get_sample_list(sampleType="all",idType="cmo",dedup = True)
        filtered_conflicts = voyager_obj.conflicts[voyager_obj.conflicts.index.isin(all_samples)]
        if filter_col:
            return filtered_conflicts[filter_col]
        else:
            return filtered_conflicts

    def generate_voyager_unpaired_table(self,voyager_obj,filter_col=None):
        """
        Filter the voyager unpaired table
        """
        all_samples = self.get_sample_list(sampleType="all",idType="cmo",dedup = True)
        filtered_conflicts = voyager_obj.unpaired[voyager_obj.unpaired.index.isin(all_samples)]
        if filter_col:
            return filtered_conflicts[filter_col]
        else:
            return filtered_conflicts

