from . import utils
import os
from cohort_utils.model import Cohort, Sample, Pair

class CRF_Handler:
    def __init__(self,**kwargs):
        self.crf = kwargs.pop("crf")
        self.meta = self.extract_meta()
        self.pairs = self.extract_pairs()
        self.cohort_id = self._extract_cohort_id()

    def _extract_cohort_id(self):
        return os.path.basename(self.crf).split(".")[0]

    def extract_meta(self):
        return utils.read_meta(self.crf)
    
    def extract_pairs(self):
        crf_table = utils.read_crf(self.crf)
        assert "TUMOR_ID" in list(crf_table)
        if not "NORMAL_ID" in list(crf_table):
            crf_table["NORMAL_ID"] = None
        return [ (row["TUMOR_ID"],row["NORMAL_ID"]) for index,row in crf_table.iterrows() ]

    def __len__(self):
        return len(list(self.pairs))

    def to_cohort(self):
        if isinstance(self.meta.get("endUsers",None),str):
            self.meta["endUsers"] = [i.strip().lower() for i in self.meta.get("endUsers").split(",")]
        if isinstance(self.meta.get("pmUsers",None),str):
            self.meta["pmUsers"] = [i.strip().lower() for i in self.meta.get("pmUsers").split(",")]
        if isinstance(self.meta.get("holdBamsAndFastqs",False),str):
            if self.meta.get("holdBamsAndFastqs").lower.strip() == "true":
                self.meta["holdBamsAndFastqs"] = True
        pairs = []
        for i in self.pairs:
            tumor_sample = Sample(id=i[0],tumor_or_normal="tumor")
            normal_sample = Sample(id=i[1],tumor_or_normal="normal")
            pairs.append(Pair(tumor_sample=tumor_sample, normal_sample=normal_sample))
        return Cohort(pairs = pairs, cohort_id = self.cohort_id, **self.meta)

