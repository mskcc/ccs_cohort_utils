import unittest
import os
import json
import tempfile
from unittest.mock import patch
os.environ["TEMPO_METADB_PROFILE"] = "local"
from cohort_utils.nats.message_handler import cohort_request_handler
from cohort_utils.pb import smile_pb2
from utils import run_test
import logging
logging.basicConfig(level=logging.DEBUG)

COHORT_JSON = "./data/json/COHORT6.cohort.json"


class MockSmileMessage:
    def __init__(self, subject, data):
        self.subject = subject
        self.data = data


class TestCohortRequestHandler(unittest.TestCase):

    def setUp(self):
        with open(COHORT_JSON) as f:
            self.cohort_data = json.load(f)
        self.cohort_id = self.cohort_data["cohortId"]

    @run_test
    def test_valid_cohort_request(self):
        msg = MockSmileMessage(
            subject="local.new-cohort-submit",
            data=json.dumps(self.cohort_data)
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            embargo_path = os.path.join(tmpdir, "embargo_dates.txt")
            with patch("cohort_utils.nats.message_handler.CRF_OUTPUT_DIR", tmpdir), \
                 patch("cohort_utils.nats.message_handler.EMBARGO_DATE_RECORD", embargo_path):
                cohort_request_handler(msg)
            expected_path = os.path.join(tmpdir, f"{self.cohort_id}.cohort.txt")
            self.assertTrue(os.path.exists(expected_path))
            with open(expected_path) as f:
                content = f.read()
            print(content)
            self.assertIn(f"#projectTitle:{self.cohort_data['projectTitle']}", content)
            self.assertIn(",".join(self.cohort_data["endUsers"]), content)

    @run_test
    def test_embargo_dates_written(self):
        msg = MockSmileMessage(
            subject="local.new-cohort-submit",
            data=json.dumps(self.cohort_data)
        )
        embargoed_samples = [s for s in self.cohort_data["samples"] if s.get("embargoDate")]
        with tempfile.TemporaryDirectory() as tmpdir:
            embargo_path = os.path.join(tmpdir, "embargo_dates.txt")
            with patch("cohort_utils.nats.message_handler.CRF_OUTPUT_DIR", tmpdir), \
                 patch("cohort_utils.nats.message_handler.EMBARGO_DATE_RECORD", embargo_path):
                cohort_request_handler(msg)
            self.assertTrue(os.path.exists(embargo_path))
            with open(embargo_path) as f:
                lines = f.read().splitlines()
            print(lines)
            self.assertEqual(lines[0], "cmoSampleId\tprimaryId\tembargoDate")
            self.assertEqual(len(lines), 1 + len(embargoed_samples))
            for sample in embargoed_samples:
                self.assertTrue(any(sample["embargoDate"] in line for line in lines))

    @run_test
    def test_no_embargo_dates_no_file(self):
        cohort_no_embargo = json.loads(json.dumps(self.cohort_data))
        for s in cohort_no_embargo["samples"]:
            s.pop("embargoDate", None)
        msg = MockSmileMessage(
            subject="local.new-cohort-submit",
            data=json.dumps(cohort_no_embargo)
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            embargo_path = os.path.join(tmpdir, "embargo_dates.txt")
            with patch("cohort_utils.nats.message_handler.CRF_OUTPUT_DIR", tmpdir), \
                 patch("cohort_utils.nats.message_handler.EMBARGO_DATE_RECORD", embargo_path):
                cohort_request_handler(msg)
            self.assertFalse(os.path.exists(embargo_path))

    @run_test
    def test_cohort_update_updates_metadata(self):
        updated_cohort = json.loads(json.dumps(self.cohort_data))
        updated_cohort["projectTitle"] = "Updated Title"
        updated_cohort["endUsers"] = ["newuser1", "newuser2"]
        with tempfile.TemporaryDirectory() as tmpdir:
            embargo_path = os.path.join(tmpdir, "embargo_dates.txt")
            output_path = os.path.join(tmpdir, f"{self.cohort_id}.cohort.txt")
            # First write the original file
            submit_msg = MockSmileMessage(
                subject="local.new-cohort-submit",
                data=json.dumps(self.cohort_data)
            )
            with patch("cohort_utils.nats.message_handler.CRF_OUTPUT_DIR", tmpdir), \
                 patch("cohort_utils.nats.message_handler.EMBARGO_DATE_RECORD", embargo_path):
                cohort_request_handler(submit_msg)
            with open(output_path) as f:
                original_lines = f.read().splitlines()
            original_data_lines = [l for l in original_lines if not l.startswith("#")]
            # Now send cohort-update with changed metadata as protobuf
            pb_msg = smile_pb2.TempoCohortUpdate()
            pb_msg.cohortId = updated_cohort["cohortId"]
            pb_msg.type = updated_cohort.get("type", "")
            pb_msg.endUsers.extend(["newuser1", "newuser2"])
            pb_msg.pmUsers.extend(updated_cohort["pmUsers"])
            pb_msg.projectTitle = "Updated Title"
            pb_msg.projectSubtitle = updated_cohort.get("projectSubtitle", "")
            update_msg = MockSmileMessage(
                subject="local.cohort-update",
                data=pb_msg.SerializeToString()
            )
            with patch("cohort_utils.nats.message_handler.CRF_OUTPUT_DIR", tmpdir), \
                 patch("cohort_utils.nats.message_handler.EMBARGO_DATE_RECORD", embargo_path):
                cohort_request_handler(update_msg)
            with open(output_path) as f:
                updated_lines = f.read().splitlines()
            updated_data_lines = [l for l in updated_lines if not l.startswith("#")]
            # Metadata should be updated
            self.assertTrue(any("Updated Title" in l for l in updated_lines))
            self.assertTrue(any("newuser1" in l for l in updated_lines))
            # Data lines should be unchanged
            self.assertEqual(original_data_lines, updated_data_lines)

    @run_test
    def test_cohort_update_no_existing_file(self):
        pb_msg = smile_pb2.TempoCohortUpdate()
        pb_msg.cohortId = self.cohort_data["cohortId"]
        pb_msg.type = self.cohort_data.get("type", "")
        pb_msg.endUsers.extend(self.cohort_data["endUsers"])
        pb_msg.pmUsers.extend(self.cohort_data["pmUsers"])
        pb_msg.projectTitle = self.cohort_data["projectTitle"]
        pb_msg.projectSubtitle = self.cohort_data.get("projectSubtitle", "")
        msg = MockSmileMessage(
            subject="local.cohort-update",
            data=pb_msg.SerializeToString()
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            embargo_path = os.path.join(tmpdir, "embargo_dates.txt")
            output_path = os.path.join(tmpdir, f"{self.cohort_id}.cohort.txt")
            with patch("cohort_utils.nats.message_handler.CRF_OUTPUT_DIR", tmpdir), \
                 patch("cohort_utils.nats.message_handler.EMBARGO_DATE_RECORD", embargo_path):
                cohort_request_handler(msg)
            self.assertTrue(os.path.exists(output_path))
            with open(output_path) as f:
                content = f.read()
            self.assertIn(f"#projectTitle:{self.cohort_data['projectTitle']}", content)

    @run_test
    def test_invalid_schema_raises(self):
        invalid_data = {"cohortId": "TEST", "samples": [{"cmoId": "C-AAAAAA-P001-d"}]}
        msg = MockSmileMessage(
            subject="local.new-cohort-submit",
            data=json.dumps(invalid_data)
        )
        self.assertRaises(Exception, cohort_request_handler, msg)

    @run_test
    def test_invalid_json_raises(self):
        msg = MockSmileMessage(
            subject="local.new-cohort-submit",
            data="not valid json"
        )
        self.assertRaises(Exception, cohort_request_handler, msg)


if __name__ == "__main__":
    unittest.main()
