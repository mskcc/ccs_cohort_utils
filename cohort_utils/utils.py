import re
import numpy as np

def categorize_id(id):
    id = normalize_id(id)
    id_type = None
    if re.match('^C-[A-Z,0-9]{6}-[MPNGTXR][0-9]{3}-d[0-9]{0,2}$',id):
        id_type = "cmoSampleName"
    elif re.match('^C-[A-Z,0-9]{6}$',id):
        id_type = "cmoPatientId"
    elif re.match('^P-[0-9]{7}$',id):
        id_type = "dmpPatientId"
    elif re.match('^P-[0-9]{7}-[TN][0-9]{2}',id):
        id_type = "dmpSampleName"
    elif re.match('^[0-9]{4,5}-[A-Z]{2}-[0-9]+$',id):
        id_type = "primaryId"
    elif re.match('^[0-9]{4,5}-[0-9]+$',id):
        id_type = "primaryId"
    elif re.match('^[0-9]{4,5}$',id):
        id_type = "requestId"
    elif re.match('^[0-9]{4,5}-[A-Z]{2}$',id):
        id_type = "requestId"
    return id_type

def normalize_id(id):
    id_normalize = id.replace("_","-")
    if id_normalize.startswith("s-"):
        id_normalize = id_normalize[2:]
    if id_normalize.startswith("IGO-"):
        id_normalize = id_normalize[4:]
    return id_normalize
