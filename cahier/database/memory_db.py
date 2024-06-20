""" In Memory Database """
from typing import Protocol

from cahier.schemas.schemas import WebId, Obj

################################################################################

class ObjMemoryInterface(Protocol):
    """ """
    
    @property
    def parent(self):
        pass
    @property
    def obj(self):
        pass

        
class ObjMemory:
    """ """
    
    def __init__(self, obj: Obj, parent: WebId):
        self.__obj = obj
        self.__parent = parent
    
    @property
    def parent(self):
        return self.__parent
    
    @property
    def obj(self):
        return self.__obj

    
db: dict[WebId, ObjMemory] = {}


def make_obj(obj: Obj, parent: WebId)->ObjMemoryInterface:
    """ """
    
    return ObjMemory(obj, parent)


def get_memory_db():
    """ """
    try:
        yield db
    finally:
        pass