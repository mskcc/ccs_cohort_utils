from cohort_utils.sampleprotobuf import SampleProtobuf_Handler
from cohort_utils.nats import EventHandler
import asyncio
from cohort_utils import utils

def send_generic_event(handler_event):
    loop = asyncio.get_event_loop()
    handler_event.send_message(loop)

def send_event(func):
    def wrapper_func(*args, **kwargs):
        msg_data = func(*args, **kwargs)
        event_type = func.__name__.split("_")[0]
        handler_event = EventHandler(type=event_type, data=msg_data)
        loop = asyncio.get_event_loop()
        handler_event.send_message(loop)
    return wrapper_func

@send_event
def bam_complete_event(id,date,status):
    return {"primaryId":id,"date":date,"status":status}

@send_event
def maf_complete_event(id,normalId,date,status):
    return {"primaryId":id,"normalPrimaryId":normalId,"date":date,"status":status}

@send_event
def qc_complete_event(id,date,status,result,reason):
    return {"primaryId":id,"date":date,"status":status,"result":result,"reason":reason}

@send_event
def cohort_complete_event(cohort_json,date=None,status=None):
    if date:
        cohort_json["date"] = date
    if status:
        cohort_json["status"] = status
    return cohort_json

def cbioportal_multisample_event(maf):
    mixed_maf = utils.read_maf(maf)
    unique_values = mixed_maf['Tumor_Sample_Barcode'].unique()
    for value in unique_values:
        # Filter rows where 'A' matches the current value
        cbioportal_singlesample_event(mixed_maf[mixed_maf['Tumor_Sample_Barcode'] == value])

@send_event
def cbioportal_singlesample_event(maf_table):
    sph = SampleProtobuf_Handler(maf_table=maf_table)
    tm = sph.generate_tempomessage()
    return tm