import pandas as pd

class VoyagerTracker:
    def __init__(self,**kwargs):
        self.file = kwargs.pop("file")
        self.table = pd.read_csv(self.file,sep="\t",header=0)
        self.table = self.table.set_index("TUMOR_ID",drop=False)