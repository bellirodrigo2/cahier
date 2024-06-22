""""""

from typing import Callable, Protocol

################################################################################


class EventHandlerInterface(Protocol):
    """"""

    def add_event_handler(self, event_name: str, callback: Callable[..., None]) -> None:
        pass

    def remove_event_handler(
        self,
        event_name: str,
    ) -> None:
        pass

    def fire_event(self, name: str, *args, **kwargs):
        pass


class EventHandlerError(Exception):
    """"""

    pass
