from . import settings, nats_send_message
#import nats_send_message
import json, jsonschema
from cohort_utils.pb import tempo_pb2
import uuid


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
        self.id_name = kwargs.pop("id_name",None)
        #if settings.TYPE_SUBJECT_MAPPING[self.type].get("id_name",None):
        if self.id_name:
            self.headers = {
                "Nats-Msg-Subject": self.subject,
                #"Nats-Msg-Id": self.data[settings.TYPE_SUBJECT_MAPPING[self.type].get("id_name")]
                "Nats-Msg-Id": self.data[self.id_name]
            }
        else:
            self.headers = {
                "Nats-Msg-Subject": self.subject,
                "Nats-Msg-Id": str(uuid.uuid4())
            }
        self._validate_schema()

    def _validate_schema(self):
        if self.schema:
            jsonschema.validators.validate(instance=self.data, schema=self.schema)
        elif not isinstance(self.data,tempo_pb2.TempoMessage):
            print(type(self.data))
            raise TypeError("Type or format of the event handler do not match the data: {} and {}".format(self.type, self.format))

    def send_message(self,loop,ignore_error=True):
        args = dict()
        args["cert"] = settings.NATS_SSL_CERTFILE
        args["key"] = settings.NATS_SSL_KEYFILE
        args["url"] = settings.METADB_NATS_URL
        args["username"] = settings.METADB_USERNAME
        args["password"] = settings.METADB_PASSWORD
        args["subject"] = self.subject
        if self.format == "json":
            args["data"] = json.dumps(self.data).encode()
        else:
            args["data"] = self.data.SerializeToString()
        if hasattr(self, 'headers'):
            args["headers"] = self.headers

        loop.run_until_complete(nats_send_message.run(loop,args, ignore_error))