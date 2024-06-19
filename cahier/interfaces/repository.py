""""""
from typing import Protocol, Any, Callable
from abc import abstractmethod

from cahier import WebId, Obj, ObjEnum

################################################################################

class RepositoryInterface(Protocol):
    
    @staticmethod
    @abstractmethod
    def bootstrap(cls)->None:
        pass
    
    def get_one_by_webid(self, webid: WebId)->Obj:
        pass
    
    def get_all_by_parent_webid(self, webid: WebId, filter = Any)->list[Obj]:
        pass

    def add_one(self, parent_webid: WebId, obj: Obj)->None:
        pass