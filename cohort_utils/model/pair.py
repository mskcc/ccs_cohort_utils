import os
from .sample import Sample

class Pair:
    def __init__(self,**kwargs):
        self.tumor_sample = kwargs.pop("tumor_sample")
        self.normal_sample = kwargs.pop("normal_sample")

        self._validate_data_types()

    def _validate_data_types(self):
        if not isinstance(self.tumor_sample,Sample):
            raise ValueError("tumor_sample must be of class Sample!")
        if not isinstance(self.normal_sample,Sample):
            raise ValueError("normal_sample must be of class Sample!")


    def get_tuple_str(self):
        return ( str(self.tumor_sample), str(self.normal_sample) )

    def __str__(self):
        return f"{str(self.tumor_sample)}__{str(self.normal_sample)}"
