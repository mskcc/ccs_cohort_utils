import os, json
with open(os.path.join(os.path.dirname(__file__), 'cohort-request.schema.json'),'r') as fh:
    COHORT_REQUEST_JSON_SCHEMA = json.load(fh)
with open(os.path.join(os.path.dirname(__file__), 'cohort-complete.schema.json'),'r') as fh:
    COHORT_COMPLETE_JSON_SCHEMA = json.load(fh)
with open(os.path.join(os.path.dirname(__file__), 'bam-complete.schema.json'),'r') as fh:
    BAM_COMPLETE_JSON_SCHEMA = json.load(fh)
with open(os.path.join(os.path.dirname(__file__), 'maf-complete.schema.json'),'r') as fh:
    MAF_COMPLETE_JSON_SCHEMA = json.load(fh)
with open(os.path.join(os.path.dirname(__file__), 'qc-complete.schema.json'),'r') as fh:
    QC_COMPLETE_JSON_SCHEMA = json.load(fh)
