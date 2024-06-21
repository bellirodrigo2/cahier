""""""
from typing import Protocol, Tuple, Any

from cahier.schemas.objects import ObjEnum
from cahier.schemas.schemas import SingleOutput, ListOutput, WebId, ObjInput

################################################################################

class AssetError(Exception):
    pass

class AssetServiceInterface(Protocol):
    
    
    def get_one_by_webid(self, webid: WebId, target_type: ObjEnum | None)->SingleOutput:
        """"""
        pass
    
    def get_all_by_webid(self, parent: ObjEnum, children: ObjEnum,
                                webid: WebId, query_dict: dict[str, Any])->ListOutput:
        """"""
        pass
    
    def add_one_and_check_parent(self, parent: ObjEnum, children: ObjEnum, webid: WebId, obj:ObjInput)->None:
        """"""
        pass
    
