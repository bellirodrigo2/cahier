""""""
from typing import Callable

################################################################################

class Event[T]:
    """"""
    def __init__(self, name: str, data: T, autofire: bool = True):
        self.data = data
        self.name = name
        if autofire:
            self.fire()

    def fire(self):
        obs = Observer()._observables
        if self.name in obs:
            obs[self.name](self)

class Observer[T]:
    """"""

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance._observables = {}
        return cls.__instance

    def observe(self, event: Event[T], callback: Callable[[T], None]):
        self.__instance._observables[event.name] = callback