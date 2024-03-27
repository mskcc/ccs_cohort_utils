from . import utils
import os
from cohort_utils.model import Cohort#, Sample, Pair
import numpy as np

class CRF_Handler:
    def __init__(self,**kwargs):
        self.crf = kwargs.pop("crf")
        #self.crj = self.extract_meta()
        #self.pairs = self.extract_pairs()
        #self.cohort_id = self._extract_cohort_id()

    def _extract_cohort_id(self):
        return os.path.basename(self.crf).split(".")[0]

    def _extract_meta(self):
        meta = utils.read_meta(self.crf)
        if isinstance(meta.get("endUsers",None),str):
            meta["endUsers"] = [i.strip().lower() for i in meta.get("endUsers").split(",")]
        if isinstance(meta.get("pmUsers",None),str):
            meta["pmUsers"] = [i.strip().lower() for i in meta.get("pmUsers").split(",")]
        if isinstance(meta.get("holdBamsAndFastqs",False),str):
            if meta.get("holdBamsAndFastqs").lower().strip() == "true":
                meta["holdBamsAndFastqs"] = True
        return meta
    
    def _extract_samples(self):
        crf_table = utils.read_crf(self.crf)
        assert "TUMOR_ID" in list(crf_table)
        if not "NORMAL_ID" in list(crf_table):
            crf_table["NORMAL_ID"] = None
        if not "PRIMARY_ID" in list(crf_table):
            crf_table["PRIMARY_ID"] = None
        if not "NORMAL_PRIMARY_ID" in list(crf_table):
            crf_table["NORMAL_PRIMARY_ID"] = None
        crf_table.rename(
            columns={
                "TUMOR_ID":"cmoId",
                "NORMAL_ID":"normalCmoId",
                "PRIMARY_ID":"primaryId",
                "NORMAL_PRIMARY_ID":"normalPrimaryId"
            }, inplace=True
        )
        crf_table = crf_table.replace({np.nan: None})
        samples = crf_table.to_dict('records')
        return samples

    def to_cohort(self):
        cohort_json = {"cohortId":self._extract_cohort_id(),**self._extract_meta(),"samples":self._extract_samples()}
        return Cohort(crj = cohort_json)

