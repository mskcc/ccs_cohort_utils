import os
from cohort_utils import schema
if 1:
    METADB_USERNAME = os.environ.get("TEMPO_METADB_USERNAME")
    METADB_PASSWORD = os.environ.get("TEMPO_METADB_PASSWORD")
    METADB_NATS_URL = "nats://smile-dev.mskcc.org:4222"
    METADB_NATS_DURABLE = os.environ.get("TEMPO_METADB_NATS_DURABLE", "")
    METADB_NATS_FILTER_SUBJECT = "MDB_STREAM.consumers.*"
    BAM_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.bam-complete"
    QC_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.qc-complete"
    MAF_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.maf-complete"
    COHORT_COMPLETE_TOPIC = "MDB_STREAM.server.tempo.wes.cohort-complete"
    CBIO_SAMPLE_UPDATE_TOPIC = "MDB_STREAM.cbio.tempo.wes.sample-update"
    NATS_SSL_CERTFILE = os.environ.get("NATS_SSL_CERTFILE")
    NATS_SSL_KEYFILE = os.environ.get("NATS_SSL_KEYFILE")
    METADB_CLIENT_TIMEOUT = 3600.0
    #METADB_NATS_NEW_REQUEST = BAM_COMPLETE_TOPIC

TYPE_SUBJECT_MAPPING = {
    "bam":{"subject":BAM_COMPLETE_TOPIC,"format":"json","schema":schema.BAM_COMPLETE_JSON_SCHEMA},
    "maf":{"subject":MAF_COMPLETE_TOPIC,"format":"json","schema":schema.MAF_COMPLETE_JSON_SCHEMA},
    "qc":{"subject":QC_COMPLETE_TOPIC,"format":"json","schema":schema.QC_COMPLETE_JSON_SCHEMA},
    "cohort":{"subject":COHORT_COMPLETE_TOPIC,"format":"json","schema":schema.COHORT_COMPLETE_JSON_SCHEMA},
    "cbioportal":{"subject":CBIO_SAMPLE_UPDATE_TOPIC,"format":"protobuf","schema":None}
}