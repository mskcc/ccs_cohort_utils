import os,copy
#from cohort_utils.model import Sample, Pair
from .pair import Pair
from .sample import Sample

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
        self._validate_data_types()

    def __len__(self):
        return len(self.pairs)

    def _load_pairs(self,pairs):
        self.pairs = []
        for i in pairs:
            if not isinstance(i,Pair):
                tumor  = Sample(cmo_id = i[0],tumor_or_normal="tumor")  if not isinstance(i[0],Sample) else i[0]
                normal = Sample(cmo_id = i[1],tumor_or_normal="normal") if not isinstance(i[1],Sample) else i[1]
                self.pairs.append(Pair(tumor_sample=tumor,normal_sample=normal))
            else:
                self.pairs.append(i)

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
        assert isinstance(self.pairs, list)
        for i in self.pairs:
            assert isinstance(i,Pair)
        assert isinstance(self.deliver_fq, bool)
        assert isinstance(self.deliver_bam, bool)
        assert isinstance(self.deliver_somatic, bool)
        assert isinstance(self.deliver_germline, bool)

    def add_pair(self, pair):
        self.pairs = self.pairs.append(pair)

    def write_crf(self,path):
        with open(path, 'w') as f:
            f.write("#endUsers:" + ",".join(self.endUsers) + "\n")
            f.write("#pmUsers:" + ",".join(self.pmUsers) + "\n")
            f.write("#projectTitle:" + self.title + "\n")
            f.write("#projectSubtitle:" + self.subtitle + "\n")
            if self.deliver_fq and self.deliver_bam:
                f.write("#holdBamsAndFastqs:false\n")
            else: f.write("#holdBamsAndFastqs:true\n")
            #for k,v in self.meta:
            #    f.write("#{}:{}".format(k,v))
            f.write("#TUMOR_ID\tNORMAL_ID\n")
            for i in pairs:
                f.write("\t".join(i.get_tuple_str(i)) + "\n")
    
    def to_json(self):
        jsonObj = dict()
        jsonObj["cohort_id"] = self.cohort_id
        for i in ["endUsers","pmUsers","projectTitle","projectSubtitle"]:
            jsonObj[i] = self.getattr(i)
        jsonObj["holdBamsAndFastqs"] = not ( self.deliver_fq | self.deliver_bam )
        return jsonObj


