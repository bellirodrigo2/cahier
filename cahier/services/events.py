""""""
from typing import Callable

from cahier.interfaces.events import EventHandlerError

################################################################################


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
            raise EventHandlerError
        self.event_handlers[event_name] = callback
    
    def remove_event_handler(self, event_name: str,)->Callable[..., None]:
        if event_name not in self.event_handlers:
            raise EventHandlerError
        return self.event_handlers.pop(event_name)
        
    def fire_event(self, name: str, *args, **kwargs):
        if name in self.event_handlers:
            try:
                self.event_handlers[name]( *args, **kwargs)
            except Exception as e:
                raise EventHandlerError(e)

if __name__ == '__main__':
    print('Event')
    
# class BaseA(EventHandler):
#     pass

# class BaseB(EventHandler):
#     pass

# a = BaseA()
# b = BaseB()

# def enter_x(x: str):
#     print(f'Entering {x=}')
# def leave_x(x: str):
#     print(f'Leaving {x=}')
# a.add_event_handler('enter', enter_x)
# BaseA().add_event_handler('leave', leave_x)

# a.fire_event('enter', 'event1')
# a.fire_event('leave', 'event1')