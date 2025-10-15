from cohort_utils.sampleprotobuf import SampleProtobuf_Handler
from cohort_utils.nats import EventHandler
import asyncio
from cohort_utils import utils

def send_event(func):
    def wrapper_func(*args, **kwargs):
        event_type = func.__name__.split("_")[0]
        if kwargs.get("id",None):
            idType = utils.categorize_id(kwargs.get("id"))
            if idType == "cmoSampleName":
                kwargs["id_name"] = "cmoId"
            else:
                kwargs["id_name"] = idType
        elif event_type == "cohort":
            kwargs["id_name"] = "cohortId"
        else:
            pass
        ignore_error = kwargs.pop('ignore_error',True)
        msg_data = func(*args, **kwargs)
        print(msg_data)
        handler_event = EventHandler(type=event_type, data=msg_data,id_name = kwargs.get("id_name",None))
        loop = asyncio.get_event_loop()
        handler_event.send_message(loop,ignore_error=ignore_error)
    return wrapper_func

@send_event
def bam_complete_event(id_name,id,date,status):
    #return {"primaryId":id,"date":date,"status":status}
    return {id_name:id,"date":date,"status":status}

@send_event
def maf_complete_event(id_name,id,normalId,date,status):
    #return {"primaryId":id,"normalPrimaryId":normalId,"date":date,"status":status}
    return {id_name:id,"normal" + id_name[0].upper() + id_name[1:]:normalId,"date":date,"status":status}

@send_event
def qc_complete_event(id_name,id,date,status,result,reason):
    #return {"primaryId":id,"date":date,"status":status,"result":result,"reason":reason}
    return {id_name:id,"date":date,"status":status,"result":result,"reason":reason}

@send_event
def cohort_complete_event(cohort_json,date=None,status=None,pipelineVersion=None,**kwargs):
    if date:
        cohort_json["date"] = date
    if status:
        cohort_json["status"] = status
    if pipelineVersion:
        cohort_json["pipelineVersion"] = pipelineVersion

    return cohort_json

def cbioportal_multisample_event(maf,ignore_error=True):
    mixed_maf = utils.read_maf(maf)
    unique_values = mixed_maf['Tumor_Sample_Barcode'].unique()
    for value in unique_values:
        # Filter rows where 'A' matches the current value
        cbioportal_singlesample_event(mixed_maf[mixed_maf['Tumor_Sample_Barcode'] == value],ignore_error=ignore_error)

@send_event
def cbioportal_singlesample_event(maf_table):
    sph = SampleProtobuf_Handler(maf_table=maf_table)
    tm = sph.generate_tempomessage()
    return tm
