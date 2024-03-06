import json, jsonschema
from cohort_utils.model import Cohort#, Sample, Pair
import cohort_utils

class CRJ_Handler:
    def __init__(self,crj_file=None,crj=None):
        if crj:
            self.crj = crj
        else:
            with open(crj_file, 'r') as f:
                self.crj = json.load(f)

    def __len__(self):
        return len(self.crj["samples"])

    def to_cohort(self):
        return Cohort(crj = self.crj)

    #def to_cohort(self):
    #    pairs = []
    #    for i in self.crj["samples"]:
    #        tumor_sample = Sample(cmoId=i.get("cmoId"),primaryId=i.get("primaryId"),tumor_or_normal="tumor")
    #        normal_sample = Sample(cmoId=i.get("normalCmoId"),primaryId=i.get("normalPrimaryId"),tumor_or_normal="normal")
    #        pairs.append(Pair(tumor_sample=tumor_sample, normal_sample=normal_sample))
    #    return Cohort(pairs = pairs, **{i:self.crj[i] for i in self.crj if i != "samples")
