import argparse
import asyncio
import logging
from nats.aio.client import Client as NATS
import argparse, sys
import asyncio
import json
import os
from nats.aio.client import Client as NATS
import ssl
import configparser
import logging
from . import nats_utils

logger = logging.getLogger(__name__)

def usage():
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", help="Subject to subscribe to")
    parser.add_argument("-s", "--servers", default=["nats://127.0.0.1:4222"], action="append", help="NATS server URLs")
    args = parser.parse_args()
    return vars(args)

async def message_handler(msg):
    data = msg.data.decode()
    logger.info(f"Received a message: {data}")

async def run(loop, args, seconds=-1):
    nc = NATS()

    options = dict()
    if args["cert"] and args["key"]:
        logger.info("Creating context based on provided cert and key")
        options["tls"] = nats_utils.create_context(args["cert"],args["key"])
    if args["username"] and args["password"]:
        logger.info(f"Connecting to NATS at {args["url"]} as {args["username"]}")
        options["servers"] = "nats://{}:{}@{}".format(args["username"],args["password"],args["url"].split("//")[1])
    else:
        logger.info(f"Connecting to NATS at {args["url"]} without authentication")
        options["servers"] = args["url"]

    logger.info(f"Connecting to NATS")
    await nc.connect(**options)
    logger.info(f"Subscribed to subject: {args["subject"]}")
    await nc.subscribe(args["subject"], cb=message_handler)

    logger.info(f"Subscribed to subject: {args['subject']}")

    try:
        if seconds >= 0:
            await asyncio.sleep(seconds)
            await nc.close()
        else:
            while True:
                await asyncio.sleep(1)
    except asyncio.CancelledError:
        await nc.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = usage()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run(loop, args))
    finally:
        loop.close()