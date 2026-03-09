from smile_client.messages.smile_message import SmileMessage
from cohort_utils.model.cohort import Cohort
from cohort_utils.schema import COHORT_REQUEST_JSON_SCHEMA
from cohort_utils.nats.settings import CRF_OUTPUT_DIR, EMBARGO_DATE_RECORD
import jsonschema
import logging
import json
import os

logger = logging.getLogger("smile_client")


def cohort_request_handler(msg: SmileMessage):
    """
    Process incoming cohort request SMILE messages.

    Expects msg.data to be a JSON-encoded cohort request compliant with
    cohort-request.schema.json. Creates a Cohort object and writes the
    result in CRF format to <CRF_OUTPUT_DIR>/<cohortId>.cohort.txt.

    Args:
        msg (SmileMessage): Message object containing subject and data
    """
    try:
        data = json.loads(msg.data)
        jsonschema.validate(instance=data, schema=COHORT_REQUEST_JSON_SCHEMA)
        cohort = Cohort(crj=data)
        crf_content = cohort.to_crf(keep_primary_ids=False)
        cohort_id = cohort.cohort["cohortId"]
        output_path = os.path.join(CRF_OUTPUT_DIR, f"{cohort_id}.cohort.txt")
        with open(output_path, "w") as f:
            f.write(crf_content)
        logger.info(f"Wrote CRF for cohort {cohort_id} to {output_path}")
        embargoed = [s for s in cohort.cohort["samples"] if s.get("embargoDate")]
        if embargoed:
            write_header = not os.path.exists(EMBARGO_DATE_RECORD)
            with open(EMBARGO_DATE_RECORD, "a") as f:
                if write_header:
                    f.write("cmoSampleId\tprimaryId\tembargoDate\n")
                for s in embargoed:
                    if s['embargoDate'] == "":
                        continue
                    f.write(f"{s.get('cmoId', '')}\t{s.get('primaryId', '')}\t{s['embargoDate']}\n")
            logger.info(f"Appended {len(embargoed)} embargo date record(s) to {EMBARGO_DATE_RECORD}")
    except Exception as e:
        logger.error(f"Error processing cohort request message: {e}")
        raise
