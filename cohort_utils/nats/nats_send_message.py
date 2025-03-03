import argparse, sys
import asyncio
import json
import os
#import signal
from nats.aio.client import Client as NATS
import ssl
import configparser
import logging
from . import nats_utils

logger = logging.getLogger(__name__)

def usage():
    parser = argparse.ArgumentParser()

    # e.g. nats-req hello -d "world" -s nats://127.0.0.1:4222 -s nats://127.0.0.1:4223
    parser.add_argument("subject", default="hello", nargs="?")
    parser.add_argument("-d", "--data", default="hello world")
    parser.add_argument("-s", "--servers", default=[], action="append")
    parser.add_argument("--creds")
    parser.add_argument("--cert")
    parser.add_argument("--key")
    parser.add_argument("--cfg")
    args = parser.parse_args()
    return vars(args)

async def run(loop, args, ignore_error=True):
    nc = NATS()

    async def error_cb(e):
        if ignore_error:
            logger.warning(e)
        else:
            logger.error(e)
            raise Exception(e)

    async def closed_cb():
        logger.warning("Connection to NATS is closed.")

    async def reconnected_cb():
        logger.warning(f"ReConnected to NATS at {nc.connected_url.netloc}...")

    options = {"error_cb": error_cb, "closed_cb": closed_cb, "reconnected_cb": reconnected_cb}

    if args.get("creds"):
        logger.warning("Using credentials")
        options["user_credentials"] = args["creds"]
    """
    config_dict = dict()
    section_header='default'
    if args.get("cfg"):
        config_parser = configparser.RawConfigParser()
        try:
            config_parser.read(args["cfg"])
            section_header=config_parser.sections()[0]
        except configparser.MissingSectionHeaderError as m:
            with open(args["cfg"],'r') as f:
                cfg_content = '[default]\n' + f.read()
            config_parser.read_string(cfg_content) 
        for i in config_parser[section_header]:
            config_dict[i] = config_parser.get(section_header,i)

                
        options["user"] = config_dict['nats.consumer_name']
        options["password"] = config_dict['nats.consumer_password']
        options["servers"] = config_dict['nats.url']
    """

    if args["cert"] and args["key"]:
        logger.info("Creating context based on provided cert and key")
        #ssl._create_default_https_context = ssl._create_unverified_context
        options["tls"] = nats_utils.create_context(args["cert"],args["key"])
        
    try:
        if args.get("url",None):
            options["servers"] = "nats://{}:{}@{}".format(args["username"],args["password"],args["url"].split("//")[1])
            logger.info(f"Connecting to NATS at {args['url']} as {args['username']}")
        await nc.connect(**options)
        logger.info(f"Connected")
    except Exception as e:
        logger.error("Error connecting")
        logger.error(e)


    # msg = await nc.request(args["subject"], args["data"].encode())
    # subject = msg.subject
    # reply = msg.reply
    # data = msg.data.decode()
    # print("Received a message on '{subject} {reply}': {data}".format(
    #     subject=subject, reply=reply, data=data))
    """
    with open(args["data"], "r") as f:
        print("loading json from {} as object {}".format(args["data"],f))
        data = json.load(f)
        print("parse json to string")
        data_str = json.dumps(data)
    print(data_str)
    """
    logger.debug('Publishing the following message:\nSubject:{}\nPayload:{}\nHeaders:{}'.format(args["subject"], args["data"], str(args.get("headers", None))))
    await nc.publish(args["subject"], args["data"], headers = args.get("headers", None))
    await nc.close()
    logger.info(f"Closing connection")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run(loop,usage()))
    finally:
        loop.close()
