import csv
#import pandas as pd

csv.register_dialect('readCRFSamples', delimiter="\t", quoting=csv.QUOTE_NONE)

def extractMeta(s):
    return s.split(":")[0].strip(), ":".join(s.split(":")[1:]).strip()

def validateString(s,char,minFields):
    if len(s.split(char)) < minFields:
        raise ValueError

def read_meta(CRF):
    meta_dict=dict()
    with open(CRF, 'r') as myFile:
        reader = csv.reader(clean_comment(myFile,removeComment=False), dialect='readCRFSamples')
        for row in reader: 
            if row[0] in ["TUMOR_ID","NORMAL_ID"]:
                continue
            else:
                try: 
                    validateString("\t".join(row),":",2)
                except:
                    pass
                else:
                    k,v = extractMeta("\t".join(row))
                    meta_dict[k]=v
    return meta_dict

def clean_comment(csvfile,comment="#",removeComment=True):
    for row in csvfile:
        s = row.replace("\"","").replace("'","").strip().split(comment)
        if s[0].strip() == "": 
            if len(s) > 0:
                if not removeComment:
                    yield "#".join(s[1:])
        else:
            #if removeComment:
            if 1:
                yield "#".join(s)

def read_crf(crf):
    rows = []
    with open(crf, 'r') as f:
        in_meta=True
        line_cursor=0
        while in_meta:
            l =  f.readline()
            l = l.strip().lstrip("\"")
            if l.startswith("#NORMAL_ID") or l.startswith("#TUMOR_ID"):
                in_meta=False
                f.seek(line_cursor)
                reader = csv.reader(clean_comment(f,removeComment=False), dialect='readCRFSamples')
                for row in reader:
                    rows.append(row)
            line_cursor = f.tell()
    return rows 


