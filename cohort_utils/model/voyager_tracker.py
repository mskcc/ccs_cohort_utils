import pandas as pd
import os

class VoyagerTempoMPGen:
    def __init__(self,**kwargs):
        self.folderPath = kwargs.pop("folderPath")
        self._load_files()

    def _load_files(self):
        for source,index_col in {"tracker":"CMO_Sample_ID","conflict":"ciTag","unpaired":"ciTag","mapping":"SAMPLE","pairing":"TUMOR_ID"}.items():
            print("loading " + source)
            setattr(self,source + "_file", os.path.join(self.folderPath,"sample_" + source + ".txt"))
            setattr(self,source, pd.read_csv(getattr(self,source + "_file"),sep="\t",header=0))
            getattr(self,source).index = getattr(self,source)[[index_col]]

    def compare(self,other):
        # for each voyager output, merge the tracker, pairing, and mapping files into one table.
        mapping_new = pd.merge(self.mapping[["SAMPLE","TARGET","FASTQ_PE1"]], self.tracker[["CMO_Sample_ID","primaryId"]],left_on="SAMPLE",right_on="CMO_Sample_ID", how="inner")
        mapping_new = pd.merge(mapping_new, self.pairing, how="left", left_on="SAMPLE", right_on="TUMOR_ID")
        mapping_new = mapping_new.groupby(['primaryId','CMO_Sample_ID','TARGET','NORMAL_ID'])['FASTQ_PE1'].apply(list).reset_index(name='FASTQ_PE1')
        
        mapping_old = pd.merge(other.mapping[["SAMPLE","TARGET","FASTQ_PE1"]], other.tracker[["CMO_Sample_ID","primaryId"]],left_on="SAMPLE",right_on="CMO_Sample_ID", how="inner")
        mapping_old = pd.merge(mapping_old, other.pairing, how="left", left_on="SAMPLE", right_on="TUMOR_ID")
        mapping_old = mapping_old.groupby(['primaryId','CMO_Sample_ID','TARGET','NORMAL_ID'])['FASTQ_PE1'].apply(list).reset_index(name='FASTQ_PE1')

        # merge the two tables and find any changes. 
        merged_mapping = pd.merge(mapping_new, mapping_old, how="outer",on="primaryId",suffixes=('_new','_old'))
        merged_mapping["dropped"] = merged_mapping['CMO_Sample_ID_new'].isnull()
        merged_mapping["added"] = merged_mapping['CMO_Sample_ID_old'].isnull()
        merged_mapping = merged_mapping.assign(bait_change = lambda x: (x["TARGET_new"] != x["TARGET_old"]) & ~(x['dropped']) & ~(x['added']))
        merged_mapping = merged_mapping.assign(cmoId_change = lambda x: (x["CMO_Sample_ID_new"] != x["CMO_Sample_ID_old"]) & ~(x['dropped']) & ~(x['added']))
        merged_mapping = merged_mapping.assign(fastq_change = lambda x: (x["FASTQ_PE1_new"] != x["FASTQ_PE1_old"]) & ~(x['dropped']) & ~(x['added']))
        merged_mapping = merged_mapping.assign(normal_change = lambda x: (x["NORMAL_ID_new"] != x["NORMAL_ID_old"]) & ~(x['dropped']) & ~(x['added']))
        
        return merged_mapping

    def get_conflicts(self,query):
        pass
    
    def get_unpaired(self,query):
        pass