import os
from cohort_utils import schema
METADB_USERNAME = os.environ.get("TEMPO_METADB_USERNAME")
METADB_PASSWORD = os.environ.get("TEMPO_METADB_PASSWORD")
NATS_SSL_CERTFILE = os.environ.get("NATS_SSL_CERTFILE")
NATS_SSL_KEYFILE = os.environ.get("NATS_SSL_KEYFILE")
METADB_NATS_DURABLE = os.environ.get("TEMPO_METADB_NATS_DURABLE", "")
METADB_PROFILE = os.environ.get("TEMPO_METADB_PROFILE","dev") # dev or prod

if METADB_PROFILE not in ["dev","prod"]:
    raise ValueError("invalid NATS_PROFILE value")

if METADB_PROFILE == "dev":
    METADB_NATS_URL = "nats://smile-dev.mskcc.org:4222"
    METADB_NATS_DURABLE = os.environ.get("TEMPO_METADB_NATS_DURABLE", "")
    METADB_NATS_FILTER_SUBJECT = "MDB_STREAM.consumers.*"
    BAM_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.bam-complete"
    QC_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.qc-complete"
    MAF_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.maf-complete"
    COHORT_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.cohort-complete"
    CBIO_SAMPLE_UPDATE_TOPIC = "MDB_STREAM.cbio.tempo.wes.sample-update"
    METADB_CLIENT_TIMEOUT = 3600.0
    #METADB_NATS_NEW_REQUEST = BAM_COMPLETE_TOPIC
else:
    METADB_NATS_URL = "nats://smile.mskcc.org:4222"
    METADB_NATS_FILTER_SUBJECT = "MDB_STREAM.consumers.*"
    BAM_COMPLETE_TOPIC = "MDB_STREAM.tempo.wes.bam-complete"
    QC_COMPLETE_TOPIC = "MDB_STREAM.tempo.wes.qc-complete"
    MAF_COMPLETE_TOPIC = "MDB_STREAM.tempo.wes.maf-complete"
    COHORT_COMPLETE_TOPIC = "MDB_STREAM.tempo.wes.cohort-complete"
    CBIO_SAMPLE_UPDATE_TOPIC = "MDB_STREAM.cbio.tempo.wes.sample-update"
    METADB_CLIENT_TIMEOUT = 3600.0


TYPE_SUBJECT_MAPPING = {
    "bam":{"subject":BAM_COMPLETE_TOPIC,"format":"json","schema":schema.BAM_COMPLETE_JSON_SCHEMA},
    "maf":{"subject":MAF_COMPLETE_TOPIC,"format":"json","schema":schema.MAF_COMPLETE_JSON_SCHEMA},
    "qc":{"subject":QC_COMPLETE_TOPIC,"format":"json","schema":schema.QC_COMPLETE_JSON_SCHEMA},
    "cohort":{"subject":COHORT_COMPLETE_TOPIC,"format":"json","schema":schema.COHORT_COMPLETE_JSON_SCHEMA},
    "cbioportal":{"subject":CBIO_SAMPLE_UPDATE_TOPIC,"format":"protobuf","schema":None}
}