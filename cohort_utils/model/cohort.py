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
from .sample import Sample
import logging
logger = logging.getLogger(__name__)

crf_cohort_sample_attr_map = {
    "TUMOR_ID":"cmoId",
    "NORMAL_ID":"normalCmoId",
    "TUMOR_PRIMARY_ID":"primaryId",
    "NORMAL_PRIMARY_ID":"normalPrimaryId",
    "ONCOTREECODE":"oncotreeCode",
    "SAMPLENAME":"sampleName",
    "INVESTIGATORSAMPLEID":"investigatorSampleId",
    "NORMAL_SAMPLENAME":"normalSampleName",
    "NORMAL_INVESTIGATORSAMPLEID":"normalInvestigatorSampleId"
}

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
        crf_string += f"#endUsers:{','.join(self.cohort['endUsers'])}\n"
        crf_string += f"#pmUsers:{','.join(self.cohort['pmUsers'])}\n"
        crf_string += f"#projectTitle:{self.cohort['projectTitle']}\n"
        if "projectSubtitle" in self.cohort:
            crf_string += f"#projectSubtitle:{self.cohort['projectSubtitle']}\n"
        crf_string += f"#deliverBam:{self.cohort['deliverBam']}\n"
        crf_string += f"#deliverFastq:{self.cohort['deliverFastq']}\n"
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
    
    def to_crf_extend(self):
        crf_string = ""
        crf_string += f"#endUsers:{','.join(self.cohort['endUsers'])}\n"
        crf_string += f"#pmUsers:{','.join(self.cohort['pmUsers'])}\n"
        crf_string += f"#projectTitle:{self.cohort['projectTitle']}\n"
        if "projectSubtitle" in self.cohort:
            crf_string += f"#projectSubtitle:{self.cohort['projectSubtitle']}\n"
        crf_string += f"#deliverBam:{self.cohort['deliverBam']}\n"
        crf_string += f"#deliverFastq:{self.cohort['deliverFastq']}\n"
        crf_string += "#TUMOR_ID\tNORMAL_ID\tPRIMARY_ID\tNORMAL_PRIMARY_ID\tONCOTREECODE\tSAMPLENAME\tINVESTIGATORSAMPLEID\tNORMAL_SAMPLENAME\tNORMAL_INVESTIGATORSAMPLEID\n"
        df = pd.DataFrame(self.cohort["samples"])
        keep_col = "cmoId|normalCmoId|primaryId|normalPrimaryId|oncotreeCode|sampleName|investigatorSampleId|normalSampleName|normalInvestigatorSampleId".split("|")
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

    def update_with_metadata_table(self,metadata_table,overwrite=False):
        newcohort = copy.deepcopy(self)
        for i in newcohort.cohort["samples"]:
            try:
                this_sample = Sample(**{k:i[k] for k in ["cmoId","primaryId"] if k in i})
                this_sample.update_sample_with_metadata(metadata_table,overwrite=overwrite)
                #logger.debug(str(this_sample.metadata))
                for k in this_sample.metadata:
                    i[k] = this_sample.metadata[k]
            except Exception as e:
                print(e)
            try:
                this_sample = Sample(**{k:i["normal" + k[0].upper() + k[1:]] for k in ["cmoId","primaryId"] if "normal" + k[0].upper() + k[1:] in i})
                this_sample.update_sample_with_metadata(metadata_table,overwrite=overwrite)
                for k in this_sample.metadata:
                    i["normal" + k[0].upper() + k[1:]] = this_sample.metadata[k]
            except Exception as e:
                print(e)
        return newcohort
    
    def update_with_smile(self,overwrite=False,additional_required_fields=["oncotreeCode"]):
        newcohort = copy.deepcopy(self)
        for i in newcohort.cohort["samples"]:
            try:
                this_sample = Sample(**{k:i[k] for k in ["cmoId","primaryId"] if k in i})
                this_sample.update_sample_with_smile(overwrite=overwrite,additional_required_fields=additional_required_fields)
                for k in this_sample.metadata:
                    i[k] = this_sample.metadata[k]
            except Exception as e:
                print(e)
            try:
                this_sample = Sample(**{k:i["normal" + k[0].upper() + k[1:]] for k in ["cmoId","primaryId"] if "normal" + k[0].upper() + k[1:] in i})
                this_sample.update_sample_with_smile(overwrite=overwrite,additional_required_fields=additional_required_fields)
                for k in this_sample.metadata:
                    if k != "oncotreeCode":
                        i["normal" + k[0].upper() + k[1:]] = this_sample.metadata[k]
            except Exception as e:
                print(e)
        return newcohort

    def _validate_schema(self,schema=None):
        if not schema:
            schema = self.schema
        jsonschema.validators.validate(instance=self.cohort, schema=schema)

    def cohort_complete_generate(self,status=None,date=None,use_cmoid=False):
        mod_cohort = copy.deepcopy(self.cohort)
        if "deliverBam" in mod_cohort:
            del mod_cohort["deliverBam"]
        if "deliverFastq" in mod_cohort:
            del mod_cohort["deliverFastq"]
        if "holdBamsAndFastqs" in mod_cohort:
            del mod_cohort["holdBamsAndFastqs"]
        if use_cmoid:
            keep_sample_fields = ["cmoId","normalCmoId"]
        else:
            keep_sample_fields = ["primaryId","normalPrimaryId"]
        for idx, i in enumerate(mod_cohort["samples"]):
            mod_cohort["samples"][idx] = {k:i[k] for k in keep_sample_fields if k in i}
        #mod_cohort["samples"][idx] = { k:utils.normalize_id(i[k]) if k in ["cmoId","normalCmoId"] else (k:i[k]) for k in keep_sample_fields }
        mod_cohort["samples"][idx] = {k:(utils.normalize_id(i[k]) if k in ["cmoId","normalCmoId"] else i[k]) for k in keep_sample_fields }
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

    def deduplicate_samples(self,main_id="cmoId"):
        self.cohort["samples"] = list({v[main_id]:v for v in self.cohort["samples"]}.values())
        return self
