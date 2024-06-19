""""""
from typing import Protocol, Callable

################################################################################


class EventInterface[T](Protocol):
    
    @property
    def name(self) -> str:
        pass
    
    @property
    def data(self) -> T:
        pass
    
    def fire(self) -> None:
        pass


class ObserverInterface[T](Protocol):
    def observe(self, event: EventInterface[T], callback: Callable[[T], None]):
        pass