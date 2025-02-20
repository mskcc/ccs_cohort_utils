import asyncio
from cohort_utils import utils
from cohort_utils.nats import SubscribeHandler

def receive_event(func):
    def wrapper_func(*args, **kwargs):
        event_type = func.__name__.split("_")[0]
        handler_event = SubscribeHandler(type=event_type)
        loop = asyncio.get_event_loop()
        handler_event.subscribe_to_stream(loop,seconds=kwargs.get("seconds",-1))
    return wrapper_func


@receive_event
def bam_subscriber():
    pass


