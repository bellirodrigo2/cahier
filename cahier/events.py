""""""
from typing import Callable, Any

# from fastapi import Request

################################################################################

class Event:
    """"""
    def __init__(self, name: str, data, autofire: bool = True):
        self.name = name
        self.data = data
        if autofire:
            self.fire()

    def fire(self):
        for observer in RequestObserver._observers:
            if self.name in observer._observables:
                observer._observables[self.name](self)


class RequestObserver:
    """"""
    _observers = []
    def __init__(self):
        self._observers.append(self)
        self._observables = {}
    def observe(self, event_name: str, callback: Callable[[Event], None]):
        self._observables[event_name] = callback
    
    def get_http(self, req):
        print(f'GET request on {req.data}')

def func_ex(word: Event):
    print(f'{word.data} HAS ARRIVED TOO')

ro = RequestObserver()
ro.observe('event1',  ro.get_http)
ro.observe('event2', func_ex)

Event('event1', ['hello', 'world'])
Event('event2', 'Jerome')