from cohort_utils.pb import tempo_pb2
import os,shutil
from . import utils

class SampleProtobuf_Handler:
    def __init__(self,**kwargs):
        if "maf_table" in kwargs: 
            self.maf_table = kwargs.pop("maf_table")
        else:
            self.maf_table = utils.read_maf(kwargs.pop("maf"))
        self.cmoSampleId, self.normalCmoSampleId = utils.get_sample_id_from_maf(self.maf_table)

    def generate_tempomessage(self):
        tempomessage = tempo_pb2.TempoMessage()
        tempomessage.cmoSampleId = self.cmoSampleId
        tempomessage.normalCmoSampleId = self.normalCmoSampleId
        for index,row in self.maf_table.iterrows():
            event = tempomessage.events.add()
            event.chromosome = str(row["Chromosome"])
            event.startPosition = row["Start_Position"]
            event.endPosition = row["End_Position"]
            event.refAllele = row["Reference_Allele"]
            event.tumorSeqAllele1 = row["Tumor_Seq_Allele1"]
            event.tumorSeqAllele2 = row["Tumor_Seq_Allele2"]
        return tempomessage
