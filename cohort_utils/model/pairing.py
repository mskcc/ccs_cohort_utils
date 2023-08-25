import pandas as pd
import numpy as np

class Pairing:
    def __init__(self,**kwargs):
        self.file = kwargs.pop("file")
        self.table = pd.read_csv(self.file,sep="\t",header=0)
        self.table = self.table.set_index("TUMOR_ID",drop=False)

    def search_tumor(self,id):
        try:
            search = self.table.loc[id]
        except KeyError as e:
            return [np.nan,np.nan]
        return [search["TUMOR_ID"],search["NORMAL_ID"]]