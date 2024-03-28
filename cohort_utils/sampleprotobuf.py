from cohort_utils.pb import tempo_pb2
import os,shutil
from . import utils
import pandas as pd

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
            all_fields = tempo_pb2.Event.DESCRIPTOR.fields
            for field in all_fields:
                if not field.type == 11:
                    continue
                sub_fields = field.message_type.fields
                subevent = getattr(event,field.name)
                for f in sub_fields:
                    if pd.isnull(row[f.name]):
                        continue
                    try:
                        if f.type < 3:
                            setattr(subevent,f.name,float(row[f.name]))
                        elif f.type in [3,4,5]:
                            setattr(subevent,f.name,int(row[f.name]))
                        elif f.type == 8:
                            val = str(row[f.name]).lower()
                            if val == "true":
                                setattr(subevent,f.name,True)
                            else:
                                setattr(subevent,f.name,False)
                        else:
                            setattr(subevent,f.name,str(row[f.name]))
                    except:
                        pass
        return tempomessage
