import os, requests, json

class Sample:
    def __init__(self,**kwargs):
        self.id = kwargs.pop("id")
        self.tumor_or_normal = kwargs.pop("tumor_or_normal")
        self._validate_data_types()

    def _validate_data_types(self):
        if not isinstance(self.id,str):
            raise ValueError("id must be a string!")
        if not self.tumor_or_normal in ["tumor","normal"]: 
            raise ValueError("tumor_or_normal must be a string!")

    def __str__(self):
        return str(self.id)


