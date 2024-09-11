import os, requests, json
import numpy as np
import math
from cohort_utils import utils

class Sample:
    def __init__(self,**kwargs):
        self.metadata = kwargs
        self._validate_data_types()

    def _validate_data_types(self):
        id = self.metadata.get("primaryId",self.metadata.get("cmoId",None))
        if not isinstance(id,str):
            raise ValueError("Cannot create Sample object without cmoId or primaryId (str)")

    def update_sample_with_metadata(self,metadata_table):
        if not self.metadata.get("primaryId",None) and self.metadata.get("cmoId",None):
            self.metadata["primaryId"] = utils.get_sample_data_from_metadata_table(metadata_table,cmoId=self.metadata["cmoId"])
        elif not self.metadata.get("cmoId",None) and self.metadata.get("primaryId",None):
            self.metadata["cmoId"] = utils.get_sample_data_from_metadata_table(metadata_table,primaryId=self.metadata["primaryId"])

    def update_sample_with_smile(self,overwrite=False,additional_required_fields=[]):
        req_fields = ["primaryId","cmoId"] + additional_required_fields
        if not isinstance(overwrite, bool):
            raise TypeError("overwrite needs to be a boolean")
        if not isinstance(additional_required_fields, list):
            raise TypeError("additional_required_fields needs to be a list")
        if not overwrite:
            missing_fields = []
            for i in req_fields:
                if i not in self.metadata:
                    missing_fields += [i]
            if len(missing_fields) > 0:
                if self.metadata.get("primaryId",None):
                    smile_data = utils.get_sample_data_from_smile(primaryId=self.metadata["primaryId"])
                else:
                    smile_data = utils.get_sample_data_from_smile(cmoId=self.metadata["cmoId"])
                for i in missing_fields:
                    if i == "cmoId":
                        self.metadata[i] = utils.nice_cmo_id(smile_data["cmoSampleName"])
                    else:
                        self.metadata[i] = smile_data[i]
        else:
            if self.metadata.get("primaryId",None):
                smile_data = utils.get_sample_data_from_smile(primaryId=self.metadata["primaryId"])
            else:
                smile_data = utils.get_sample_data_from_smile(cmoId=self.metadata["cmoId"])
            for i in req_fields:
                if i == "cmoId":
                    self.metadata[i] = utils.nice_cmo_id(smile_data["cmoSampleName"])
                elif i == "primaryId" and self.metadata.get("primaryId",None):
                    pass
                else:
                    self.metadata[i] = smile_data[i]
    
    
    def __str__(self):
        return str(self.cmoId)


