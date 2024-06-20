""""""
from typing import Callable
from ..interfaces.events import EventHandlerInterface, EventHandlerError

class EventHandler():
    """"""
    
    event_handlers: dict[str, Callable[..., None]] = {}
    
    @classmethod
    def add_event_handler(self, event_name: str, callback: Callable[..., None]):
        pass
    
    def fire_event(self, name: str, *args, **kwargs):
        def fire_event(name: str, *args, **kwargs):
            if name in self.event_handlers:
                try:
                    self.event_handlers[name]( *args, **kwargs)
                except Exception as e:
                    raise EventHandlerError(e)
        return fire_event
