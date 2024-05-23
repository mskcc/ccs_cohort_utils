from . import settings, nats_send_message
#import nats_send_message
import json, jsonschema
from cohort_utils.pb import tempo_pb2

class EventHandler:
    def __init__(self,**kwargs):
        """
        Need type and data (json or protobuf object)
        """
        self.type = kwargs.pop("type")
        if self.type not in settings.TYPE_SUBJECT_MAPPING.keys():
            raise ValueError("Value for self.type in EventHandler class needs to be one of the following: {}".format(", ".join(settings.TYPE_SUBJECT_MAPPING.keys())))
        self.subject = settings.TYPE_SUBJECT_MAPPING[self.type]["subject"]
        self.format = settings.TYPE_SUBJECT_MAPPING[self.type]["format"]
        self.schema = settings.TYPE_SUBJECT_MAPPING[self.type]["schema"]
        self.data = kwargs.pop("data")
        self._validate_schema()

    def _validate_schema(self):
        if self.schema:
            jsonschema.validators.validate(instance=self.data, schema=self.schema)
        elif not isinstance(self.data,tempo_pb2.TempoMessage):
            print(type(self.data))
            raise TypeError("Type or format of the event handler do not match the data: {} and {}".format(self.type, self.format))

    def send_message(self,loop):
        args = dict()
        args["cert"] = settings.NATS_SSL_CERTFILE
        args["key"] = settings.NATS_SSL_KEYFILE
        args["servers"] = "nats://{}:{}@{}".format(settings.METADB_USERNAME,settings.METADB_PASSWORD,settings.METADB_NATS_URL.split("//")[1])
        args["subject"] = self.subject
        if self.format == "json":
            args["data"] = json.dumps(self.data).encode()
        else:
            args["data"] = self.data.SerializeToString()
        loop.run_until_complete(nats_send_message.run(loop,args, False))