""""""
from typing import Callable

class EventHandlerError(Exception):
    pass

event_handlers = {}

def add_event_handler(event_name: str, callback: Callable[..., None]):
    """"""
    event_handlers[event_name] = callback

def make_event(error_handler: Callable[[Exception], None] | None):
    """"""
    def fire_event(name: str, *args, **kwargs):
        if name in event_handlers:
            try:
                event_handlers[name]( *args, **kwargs)
            except Exception as e:
                if error_handler:
                    error_handler(e)
                raise EventHandlerError()
    return fire_event