import os, requests, json
import numpy as np
import math

class Sample:
    def __init__(self,**kwargs):
        self.id = kwargs.pop("id")
        self.tumor_or_normal = kwargs.pop("tumor_or_normal")
        self.valid_id = False
        self._validate_data_types()

    def _validate_data_types(self):
        if not isinstance(self.id,str):
            if self.tumor_or_normal == "tumor" or (not np.isnan(self.id)):
                raise ValueError(f"{self.tumor_or_normal} id invalid: {str(self.id)}")
        if not self.tumor_or_normal in ["tumor","normal"]: 
            raise ValueError("tumor_or_normal must be either of these values: tumor, normal")

    def __str__(self):
        return str(self.id)


