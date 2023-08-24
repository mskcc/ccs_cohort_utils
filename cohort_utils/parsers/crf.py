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
        tumors = list()
        normals = list()
        rows = utils.read_crf(self.crf) 
        tumor_col = 0 if rows[0][0] == "TUMOR_ID" else 1
        normal_col = 1 if tumor_col == 0 else 0
        for row in rows[1:]:
            tumors.append(row[tumor_col])
            normals.append(row[normal_col])
        return [ (k,v) for k,v in zip(tumors,normals) ]

    def __len__(self):
        return len(list(self.pairs))

    def to_cohort(self):
        pairs = []
        for i in self.pairs:
            tumor_sample = Sample(id=i[0],tumor_or_normal="tumor")
            normal_sample = Sample(id=i[1],tumor_or_normal="normal")
            pairs.append(Pair(tumor_sample=tumor_sample, normal_sample=normal_sample))
        return Cohort(pairs = pairs, cohort_id = self.cohort_id, **self.meta) 

