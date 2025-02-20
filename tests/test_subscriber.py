import unittest
import pandas as pd
import json,os
os.environ["TEMPO_METADB_PROFILE"]="local"
print(os.environ.get("METADB_PROFILE"))
import cohort_utils
import asyncio
from nats.aio.client import Client as NATS
import logging
from utils import run_test
logging.basicConfig(level=logging.DEBUG)



class TestSubscriber(unittest.TestCase):

    @run_test
    def test_subscriber(self):
        cohort_utils.subscriber.bam_subscriber("bam",seconds=10)

if __name__ == "__main__":
    unittest.main()
