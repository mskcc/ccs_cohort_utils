from cohort_utils.sampleprotobuf import SampleProtobuf_Handler
from cohort_utils.nats import EventHandler
import asyncio
from cohort_utils import utils

def send_generic_event(handler_event):
    loop = asyncio.get_event_loop()
    handler_event.send_message(loop)

def bam_complete_event(id,date,status):
    x = EventHandler(type="bam",data={"primaryId":id,"date":date,"status":status})
    send_generic_event(x)

def maf_complete_event(id,normalId,date,status):
    x = EventHandler(type="maf",data={"primaryId":id,"normalPrimaryId":normalId,"date":date,"status":status})
    send_generic_event(x)

def qc_complete_event(id,date,status,result,reason):
    x = EventHandler(type="qc",data={"primaryId":id,"date":date,"status":status,"result":result,"reason":reason})
    send_generic_event(x)

def cohort_complete_event(cohort_json,date=None,status=None):
    if date:
        cohort_json["date"] = date
    if status:
        cohort_json["status"] = status
    x = EventHandler(type="cohort",data=cohort_json)
    send_generic_event(x)

def cbio_multisample_event(maf):
    mixed_maf = utils.read_maf(maf)
    unique_values = mixed_maf['Tumor_Sample_Barcode'].unique()
    for value in unique_values:
        # Filter rows where 'A' matches the current value
        cbio_singlesample_event(mixed_maf[mixed_maf['Tumor_Sample_Barcode'] == value])
        

def cbio_singlesample_event(maf_table):
    sph = SampleProtobuf_Handler(maf_table=maf_table)
    tm = sph.generate_tempomessage()
    x = EventHandler(type="cbioportal",data=tm)
    send_generic_event(x)