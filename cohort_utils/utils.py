import re
import numpy as np
import csv
import requests
import pandas as pd
import logging
logger = logging.getLogger(__name__)


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
    elif re.match('^[0-9]{4,5}-[A-Z]{1,2}-[0-9]+$',id):
        id_type = "primaryId"
    elif re.match('^[0-9]{4,5}-[0-9]+$',id):
        id_type = "primaryId"
    elif re.match('^[0-9]{4,5}$',id):
        id_type = "requestId"
    elif re.match('^[0-9]{4,5}-[A-Z]{1,2}$',id):
        id_type = "requestId"
    return id_type

def normalize_id(id):
    id_normalize = id.replace("_","-")
    if id_normalize.startswith("s-"):
        id_normalize = id_normalize[2:]
    if id_normalize.startswith("IGO-"):
        id_normalize = id_normalize[4:]
    return id_normalize

def nice_cmo_id(id):
    id_nice = id.replace("-","_")
    if not id_nice.startswith("s_"):
        id_nice = "s_" + id_nice
    return id_nice


csv.register_dialect('maf', delimiter="\t", quoting=csv.QUOTE_NONE)

def read_maf(path):
    maf_data = pd.read_csv(path,sep="\t",header=0)
    return maf_data

def get_sample_id_from_maf(maf_table):
    tumor_id = list(maf_table.Tumor_Sample_Barcode.unique())
    normal_id = list(maf_table.Matched_Norm_Sample_Barcode.unique())
    if len(tumor_id) == 1 and len(normal_id) == 1:
        return tumor_id[0], normal_id[0]
    else:
        print(tumor_id)
        print(normal_id)
        raise ValueError("More or less than one tumor_id or normal_id in the maf")

cbio_maf_columns = [
    "Chromosome",
    "Start_Position",
    "End_Position",
    "Reference_Allele",
    "Tumor_Seq_Allele1",
    "Tumor_Seq_Allele2",
]

def filter_data_maf_columns(maf_data,maf_columns=cbio_maf_columns):
    header = maf_data[0]
    keep_col = [ True if i in maf_columns else False for i in header ]
    filtered_maf_data = [ [ r[i] for i in range(len(keep_col)) if keep_col[i] ] for r in maf_data ]
    return filtered_maf_data

def convert_cmoId_to_primaryId(id,metadata_table=None):
    query = id.replace("_","-")
    if query.startswith("s-C"):
        query = query[2:]
    result = None
    try:
        logger.debug("Converting cmoId {} to primaryId using local metadata table".format(query))
        result = metadata_table[metadata_table['cmoSampleName'].isin([id])]['primaryId'].tolist()[0]
    except Exception as e:
        logger.debug("cmoId {} not found in local metadata table".format(query))
        logger.debug("Converting cmoId {} to primaryId using smile query".format(query))
        result = search_smile_inputid(query).get("primaryId",None)
    return result

def convert_primaryId_to_cmoId(id,metadata_table=None):
    query = id
    result = None
    try:
        logger.debug("Converting primaryId {} to cmoId using local metadata table".format(query))
        result = metadata_table[metadata_table['primaryId'].isin([query])]['cmoSampleName'].tolist()[0]
    except Exception as e:
        logger.debug("primaryId {} not found in local metadata table".format(query))
        logger.debug("Converting primaryId {} to cmoId using smile query".format(query))
        result = search_smile_inputid(query).get("cmoSampleName",None)
    return result

def get_sample_data_from_metadata_table(metadata_table,cmoId=None,primaryId=None):
    if primaryId:
        result = metadata_table[metadata_table['primaryId'].isin([primaryId])]['cmoSampleName'].tolist()[0]
    elif cmoId:
        result = metadata_table[metadata_table['cmoSampleName'].isin([cmoId])]['primaryId'].tolist()[0]
    else:
        logger.error("cmoId or primaryId required for input")
        raise ValueError("cmoId or primaryId required for input")
    return result

def get_sample_data_from_smile(cmoId=None,primaryId=None):
    if primaryId:
        query = primaryId
    elif cmoId:
        query = normalize_id(cmoId)
    else:
        logger.error("cmoId or primaryId required for input")
        raise ValueError("cmoId or primaryId required for input")
    result = search_smile_inputid(query)
    keep_fields = ["primaryId","cmoSampleName","sampleName","investigatorSampleId","oncotreeCode"]
    result_final = {k:result[k] for k in result if k in keep_fields}
    return result_final

def search_smile_inputid(query):
    #apiRoute = "{}/{}/{}".format(SMILE_REST_ENDPOINT,"sampleById",query)
    apiRoute = "{}/{}/{}".format("http://smile.mskcc.org:3000","sampleById",query)
    sample_metadata = requests.get(apiRoute, timeout=360000).json()
    return sample_metadata

def get_oncotreeCode(query):
    result = search_smile_inputid(normalize_id(query)).get("oncotreeCode",None)
    return result

def search_inputid_alt(id,metadata_table):
    if categorize_id(id) == "cmoSampleName":
        pass

def clean_nones(value):
    """
    Recursively remove all None values from dictionaries and lists, and returns
    the result as a new dictionary or list.
    """
    if isinstance(value, list):
        return [clean_nones(x) for x in value if x is not None]
    elif isinstance(value, dict):
        return {
            key: clean_nones(val)
            for key, val in value.items()
            if val is not None
        }
    else:
        return value
