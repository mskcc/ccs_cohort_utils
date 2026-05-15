import pandas as pd
import os

REQUIRED_COLUMNS = {
    "tracker": ["CMO_Sample_ID", "primaryId"],
    "conflict": ["ciTag", "cmoPatientId", "primaryId", "sampleClass", "runMode", "sampleType", "baitSet", "runDate", "Conflict Reason"],
    "unpaired": ["ciTag", "cmoPatientId", "primaryId", "sampleClass", "runMode", "sampleType", "baitSet", "runDate", "Possible Reason?"],
    "mapping": ["SAMPLE", "TARGET", "FASTQ_PE1", "FASTQ_PE2"],
    "pairing": ["TUMOR_ID", "NORMAL_ID"],
}

CROSS_FILE_CHECKS = [  # used by _validate for cross-file consistency (Task 2)
    ("mapping", "SAMPLE"),
    ("pairing", "TUMOR_ID"),
    ("pairing", "NORMAL_ID"),
    ("conflict", "ciTag"),
    ("unpaired", "ciTag"),
]

class VoyagerTempoMPGen:
    def __init__(self,**kwargs):
        self.folderPath = kwargs.pop("folderPath")
        self._load_files()
        self._validate()

    def _load_files(self):
        for source, index_col in {"tracker": "CMO_Sample_ID", "conflict": "ciTag", "unpaired": "ciTag", "mapping": "SAMPLE", "pairing": "TUMOR_ID"}.items():
            print("loading " + source)
            setattr(self, source + "_file", os.path.join(self.folderPath, "sample_" + source + ".txt"))
            setattr(self, source, pd.read_csv(getattr(self, source + "_file"), sep="\t", header=0))
            df = getattr(self, source)
            if index_col in df.columns:
                df.index = df[[index_col]]

    def _validate(self):
        errors = []
        for name, required in REQUIRED_COLUMNS.items():
            df = getattr(self, name)
            missing = [c for c in required if c not in df.columns]
            if missing:
                errors.append(f"{name}: missing columns {missing}")
        if "CMO_Sample_ID" in self.tracker.columns:
            tracker_ids = set(self.tracker["CMO_Sample_ID"])
            for file_name, col_name in CROSS_FILE_CHECKS:
                df = getattr(self, file_name)
                if col_name in df.columns:
                    unknown = set(df[col_name]) - tracker_ids
                    if unknown:
                        errors.append(f"{file_name}: {col_name} values not in tracker: {unknown}")
        if errors:
            raise ValueError("VoyagerTempoMPGen validation failed:\n" + "\n".join(errors))

    def compare(self,other):
        mapping_new = pd.merge(self.mapping[["SAMPLE","TARGET","FASTQ_PE1"]], self.tracker[["CMO_Sample_ID","primaryId"]],left_on="SAMPLE",right_on="CMO_Sample_ID", how="inner")
        mapping_new = pd.merge(mapping_new, self.pairing, how="left", left_on="SAMPLE", right_on="TUMOR_ID")
        mapping_new = mapping_new.groupby(['primaryId','CMO_Sample_ID','TARGET','NORMAL_ID'])['FASTQ_PE1'].apply(list).reset_index(name='FASTQ_PE1')

        mapping_old = pd.merge(other.mapping[["SAMPLE","TARGET","FASTQ_PE1"]], other.tracker[["CMO_Sample_ID","primaryId"]],left_on="SAMPLE",right_on="CMO_Sample_ID", how="inner")
        mapping_old = pd.merge(mapping_old, other.pairing, how="left", left_on="SAMPLE", right_on="TUMOR_ID")
        mapping_old = mapping_old.groupby(['primaryId','CMO_Sample_ID','TARGET','NORMAL_ID'])['FASTQ_PE1'].apply(list).reset_index(name='FASTQ_PE1')

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
