from smile_client.messages.smile_message import SmileMessage
from cohort_utils.model.cohort import Cohort
from cohort_utils.schema import COHORT_REQUEST_JSON_SCHEMA
from cohort_utils.nats.settings import CRF_OUTPUT_DIR, EMBARGO_DATE_RECORD
from cohort_utils.pb import smile_pb2
from google.protobuf.json_format import MessageToDict
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
        if msg.subject.endswith("cohort-update") and isinstance(msg.data, bytes):
            pb_msg = smile_pb2.TempoCohortUpdate()
            pb_msg.ParseFromString(msg.data)
            data = MessageToDict(pb_msg, preserving_proto_field_name=True)
            data.setdefault("samples", [{"cmoId": "PLACEHOLDER"}])
            if "date" in data:
                del data["date"]
        else:
            data = msg.data if isinstance(msg.data, dict) else json.loads(msg.data)
        jsonschema.validate(instance=data, schema=COHORT_REQUEST_JSON_SCHEMA)
        cohort = Cohort(crj=data)
        crf_content = cohort.to_crf(keep_primary_ids=False)
        cohort_id = cohort.cohort["cohortId"]
        output_path = os.path.join(CRF_OUTPUT_DIR, f"{cohort_id}.cohort.txt")
        is_update = msg.subject.endswith("cohort-update") and os.path.exists(output_path)
        if is_update:
            with open(output_path, "r") as f:
                existing_lines = f.read().splitlines(keepends=True)
            new_header_lines = [l for l in crf_content.splitlines(keepends=True) if l.startswith("#")]
            existing_data_lines = [l for l in existing_lines if not l.startswith("#")]
            final_content = "".join(new_header_lines + existing_data_lines)
        else:
            final_content = crf_content
        with open(output_path, "w") as f:
            f.write(final_content)
        logger.info(f"{'Updated metadata in' if is_update else 'Wrote'} CRF for cohort {cohort_id} to {output_path}")
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
