import os
from cohort_utils import schema
METADB_USERNAME = os.environ.get("TEMPO_METADB_USERNAME")
METADB_PASSWORD = os.environ.get("TEMPO_METADB_PASSWORD")
NATS_SSL_CERTFILE = os.environ.get("NATS_SSL_CERTFILE")
NATS_SSL_KEYFILE = os.environ.get("NATS_SSL_KEYFILE")
METADB_NATS_DURABLE = os.environ.get("TEMPO_METADB_NATS_DURABLE", "")
METADB_PROFILE = os.environ.get("TEMPO_METADB_PROFILE","dev") # dev or prod

print(METADB_PROFILE)
if METADB_PROFILE not in ["dev","prod","local"]:
    
    raise ValueError("invalid NATS_PROFILE value")

if METADB_PROFILE == "dev":
    METADB_NATS_URL = "nats://smile-dev.mskcc.org:4222"
    METADB_NATS_FILTER_SUBJECT = "MDB_STREAM.consumers.*"
    BAM_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.bam-complete"
    QC_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.qc-complete"
    MAF_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.maf-complete"
    COHORT_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.cohort-complete"
    CBIO_SAMPLE_UPDATE_TOPIC = "CBIO_STREAM.cbio.tempo.sample-genomics"
    METADB_CLIENT_TIMEOUT = 3600.0
    #METADB_NATS_NEW_REQUEST = BAM_COMPLETE_TOPIC
elif METADB_PROFILE == "local":
    METADB_NATS_URL = "nats://127.0.0.1:4222"
    METADB_CLIENT_TIMEOUT = 3600.0
    METADB_USERNAME = None
    METADB_PASSWORD = None
    NATS_SSL_CERTFILE = None
    NATS_SSL_KEYFILE = None
    BAM_COMPLETE_TOPIC = "local.bam-complete"
    QC_COMPLETE_TOPIC = None
    MAF_COMPLETE_TOPIC = None
    COHORT_COMPLETE_TOPIC = None
    CBIO_SAMPLE_UPDATE_TOPIC = None
else:
    METADB_NATS_URL = "nats://smile.mskcc.org:4222"
    METADB_NATS_FILTER_SUBJECT = "MDB_STREAM.consumers.*"
    BAM_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.bam-complete"
    QC_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.qc-complete"
    MAF_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.maf-complete"
    COHORT_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.cohort-complete"
    CBIO_SAMPLE_UPDATE_TOPIC = "CBIO_STREAM.cbio.tempo.sample-genomics"
    METADB_CLIENT_TIMEOUT = 3600.0


TYPE_SUBJECT_MAPPING = {
    "bam":{"subject":BAM_COMPLETE_TOPIC,"format":"json","schema":schema.BAM_COMPLETE_JSON_SCHEMA,"id_name":"primaryId"},
    "maf": {"subject": MAF_COMPLETE_TOPIC, "format": "json", "schema": None, "id_name": "cmoSampleId"},
    "qc":{"subject":QC_COMPLETE_TOPIC,"format":"json","schema":schema.QC_COMPLETE_JSON_SCHEMA,"id_name":"primaryId"},
    "cohort":{"subject":COHORT_COMPLETE_TOPIC,"format":"json","schema":schema.COHORT_COMPLETE_JSON_SCHEMA,"id_name":"cohortId"},
    "cbioportal":{"subject":CBIO_SAMPLE_UPDATE_TOPIC,"format":"protobuf","schema":None}
}
