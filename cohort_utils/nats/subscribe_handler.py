from . import settings, nats_subscriber
#import nats_send_message
import json, jsonschema
from cohort_utils.pb import tempo_pb2
import uuid


class SubscribeHandler:
    def __init__(self,**kwargs):
        """
        Need type and data (json or protobuf object)
        """
        self.type = kwargs.pop("type")
        if self.type not in settings.TYPE_SUBJECT_MAPPING.keys():
            raise ValueError("Value for self.type in SubscribeHandler class needs to be one of the following: {}".format(", ".join(settings.TYPE_SUBJECT_MAPPING.keys())))
        self.subject = settings.TYPE_SUBJECT_MAPPING[self.type]["subject"]
        
    def subscribe_to_stream(self,loop,seconds=-1):
        args = dict()
        args["cert"] = settings.NATS_SSL_CERTFILE
        args["key"] = settings.NATS_SSL_KEYFILE
        args["url"] = settings.METADB_NATS_URL
        args["username"] = settings.METADB_USERNAME
        args["password"] = settings.METADB_PASSWORD
        args["subject"] = self.subject
        
        loop.run_until_complete(nats_subscriber.run(loop,args, seconds=seconds))