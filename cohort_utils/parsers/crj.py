import json, jsonschema
from cohort_utils.model import Cohort, Sample, Pair

class CRJ_Handler:
    def __init__(self,crj,schema):
        self.crj = crj
        self.schema = schema
    
    def _validate_schema(self):
        jsonschema.validators.validate(instance=self.crj, schema=self.schema)

    def __len__(self):
        return len(self.crj["manifest"])

    def to_cohort(self):
        pairs = []
        for i in self.crj["manifest"]:
            tumor_sample = Sample(id=i,tumor_or_normal="tumor")
            normal_sample = Sample(id=self.crj["manifest"][i]["NORMAL_ID"],tumor_or_normal="normal")
            pairs.append(Pair(tumor_sample=tumor_sample, normal_sample=normal_sample))
        return Cohort(pairs = pairs, cohort_id = self.crj["cohort_id"], **self.crj["meta"])