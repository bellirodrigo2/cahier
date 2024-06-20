""""""
from typing import Callable
from abc import ABC, abstractmethod
################################################################################

class EventHandlerInterface(ABC):
    """"""
    @classmethod
    @abstractmethod
    def add_event_handler(self, event_name: str, callback: Callable[..., None]):
        pass
    
    abstractmethod
    def fire_event(self, name: str, *args, **kwargs):
        pass
    
class EventHandlerError(Exception):
    """"""
    pass
