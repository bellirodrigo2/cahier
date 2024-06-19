""""""
from typing import Protocol, Tuple

from cahier import ObjEnum, SingleOutput, ListOutput, WebId, Obj

from .events import EventInterface

################################################################################

class AssetError(Exception):
    pass

PreReadOneEventInterface = EventInterface[Tuple[ObjEnum, WebId]]
PostReadOneEventInterface = EventInterface[Obj]

class AssetServiceInterface(Protocol):
    
    
    def get_one_by_webid(self, webid: WebId, target_type: ObjEnum | None)->SingleOutput:
        """"""
        pass
    
    def get_all_by_parentwebid_and_type(self, children_type: ObjEnum, parent_webid: WebId, parent_type: ObjEnum | None)->ListOutput:
        """"""
        pass
    
    def add_one_and_check_parent(self, parent_type: ObjEnum, parent_webid: WebId, obj:ObjInput)->None:
        """"""
        pass
    
