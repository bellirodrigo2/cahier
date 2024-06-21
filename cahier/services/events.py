""""""
from typing import Callable

from cahier.interfaces.events import EventHandlerError

################################################################################

# import inspect
# print(inspect.signature(foo))
# como fazer pra checar durante compilação... dados enviados para fire x handlers ????

class EventHandler():
    """"""
    instance = None
    event_handlers: dict[str, Callable[..., None]] = {}

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def add_event_handler(self, event_name: str, callback: Callable[..., None])->None:
        if event_name in self.event_handlers:
            raise EventHandlerError(f'Event Handler for event {event_name=} already registered')
        self.event_handlers[event_name] = callback
    
    def remove_event_handler(self, event_name: str,)->Callable[..., None]:
        if event_name not in self.event_handlers:
            raise EventHandlerError(f'Event Handler for event {event_name=} does not exists')
        return self.event_handlers.pop(event_name)
        
    def fire_event(self, name: str, *args, **kwargs):
        if name in self.event_handlers:
            try:
                self.event_handlers[name]( *args, **kwargs)
            except Exception as e:
                raise EventHandlerError(e)

if __name__ == '__main__':
    pass