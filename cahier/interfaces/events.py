""""""
from typing import Protocol, Callable

################################################################################


class EventInterface(Protocol):
    @property
    def data(self) -> None:
        pass
    
    def fire(self) -> None:
        pass


class ObserverInterface(Protocol):
    def observe(self, event_name: str, callback: Callable[[EventInterface], None]):
        pass