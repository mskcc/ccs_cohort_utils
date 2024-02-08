import os,copy,sys
from .pair import Pair
from .sample import Sample
import pandas as pd
import json, jsonschema


class Cohort:
    def __init__(self,**kwargs):
        self.cohort_id = kwargs.pop("cohort_id")
        self.endUsers = kwargs.pop("endUsers",[])
        self.pmUsers = kwargs.pop("pmUsers",[])
        self.title = kwargs.pop("projectTitle","")
        self.subtitle = kwargs.pop("projectSubtitle","")
        self._load_pairs(kwargs.pop("pairs",[]))
        holdBamsAndFastqs = kwargs.pop("holdBamsAndFastqs",False)
        self.deliver_fq = kwargs.pop("deliver_fq", not holdBamsAndFastqs)
        self.deliver_bam = kwargs.pop("deliver_bam", not holdBamsAndFastqs)
        self.deliver_somatic = kwargs.pop("deliver_somatic",True)
        self.deliver_germline = kwargs.pop("deliver_germline",False)
        self.type = kwargs.pop("type","investigator")
        self._validate_data_types()

    def __len__(self):
        return len(self.pairs)

    def _load_pairs(self,pairs):
        self.pairs = dict()
        for i in pairs:
            if not isinstance(i,Pair):
                tumor  = Sample(id = i[0],tumor_or_normal="tumor")  if not isinstance(i[0],Sample) else i[0]
                normal = Sample(id = i[1],tumor_or_normal="normal") if not isinstance(i[1],Sample) else i[1]
                self.pairs[i[0]] = Pair(tumor_sample=tumor,normal_sample=normal)
            else:
                self.pairs[i.tumor_sample.id] = i

    def _validate_data_types(self):
        assert isinstance(self.cohort_id,str)
        assert isinstance(self.pmUsers,list)
        for i in self.pmUsers:
            assert isinstance(i,str)
        assert isinstance(self.endUsers,list)
        for i in self.endUsers:
            assert isinstance(i,str)
        assert isinstance(self.title,str)
        assert isinstance(self.subtitle,str)
        assert isinstance(self.pairs, dict)
        for i in self.pairs:
            assert isinstance(i,str)
            assert isinstance(self.pairs[i],Pair)
        assert isinstance(self.deliver_fq, bool)
        assert isinstance(self.deliver_bam, bool)
        assert isinstance(self.deliver_somatic, bool)
        assert isinstance(self.deliver_germline, bool)
        assert isinstance(self.type, str)
        assert self.type in ["operational","investigator"]

    def add_pair(self, pair):
        self.pairs = self.pairs.append(pair)

    def to_crf(self,location=sys.stdout):
        print(f"#endUsers:{','.join(self.endUsers)}",file=location)
        print(f"#pmUsers:{','.join(self.pmUsers)}",file=location)
        print(f"#projectTitle:{self.title}",file=location)
        print(f"#projectSubtitle:{self.subtitle}",file=location)
        if self.deliver_fq and self.deliver_bam:
            print("#holdBamsAndFastqs:false",file=location)
        else: print("#holdBamsAndFastqs:true",file=location)
        print("#TUMOR_ID\tNORMAL_ID",file=location)
        for i in self.pairs:
            print("\t".join(self.pairs[i].get_tuple_str()))

    def to_json(self):
        jsonObj = dict()
        jsonObj["cohort_id"] = self.cohort_id
        jsonObj["meta"] = dict()
        jsonObj["manifest"] = dict()
        for i in ["endUsers","pmUsers","type"]:
            jsonObj["meta"][i] = getattr(self,i)
        jsonObj["meta"]["projectTitle"] =  getattr(self,"title")
        jsonObj["meta"]["projectSubtitle"] = getattr(self,"subtitle")
        jsonObj["holdBamsAndFastqs"] = not ( self.deliver_fq | self.deliver_bam )
        for i in self.pairs:
            jsonObj["manifest"][str(self.pairs[i].tumor_sample)] = {"TUMOR_ID":str(self.pairs[i].tumor_sample),"NORMAL_ID":str(self.pairs[i].normal_sample)}
        return jsonObj

    def reconcile_cohort_pairing(self,pairing):
        newcohort = copy.deepcopy(self)
        for i in newcohort.pairs:
            [t_id,n_id] = pairing.search_tumor(i)
            if not pd.isnull(t_id):
                newcohort.pairs[i].tumor_sample.valid_id = True
            if n_id == newcohort.pairs[i].normal_sample.id:
                newcohort.pairs[i].normal_sample.valid_id = True
                newcohort.pairs[i].valid_normal = True
            elif pd.isnull(newcohort.pairs[i].normal_sample.id):
                if not pd.isnull(n_id):
                    newcohort.pairs[i].normal_sample = Sample(id=n_id,tumor_or_normal="normal")
                    newcohort.pairs[i].normal_sample.valid_id = True
                    newcohort.pairs[i].valid_normal = True
        return newcohort

    def is_valid(self):
        is_valid = True
        if not all([i.valid_normal for i in self.pairs.values()]):
            is_valid = False
        if not all([i.tumor_sample.valid_id and i.normal_sample.valid_id for i in self.pairs.values()]):
            is_valid = False
        return is_valid
