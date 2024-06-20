""""""
from typing import Tuple, Callable

from cahier import AssetServiceInterface, RepositoryInterface
from cahier import WebId, ObjEnum, Obj, SingleOutput, ListOutput

from cahier import  make_single_output, make_list_output

from ..interfaces.events import EventHandlerInterface

################################################################################
class EventHandlerError(Exception):
        pass
class AssetService:
    """"""

    event_handlers: dict[str, Callable[..., None]] = {}
    
    def __init__(self,
            get_repo: Callable[[], RepositoryInterface],
            ev_handler: EventHandlerInterface, #TEM QUE SER CALLABLE ?? VAI SER INJETADO ?
        ) -> None:
        self.__get_repo = get_repo
        self.ev_handler = ev_handler
    
    def _get_one(self, webid: WebId)->Obj:
        repo: RepositoryInterface = self.__get_repo()
        return repo.get_one_by_webid(webid=webid)
    
    def _get_all(self, parent_webid: WebId)->list[Obj]:
        repo: RepositoryInterface = self.__get_repo()
        return repo.get_all_by_parent_webid(webid=parent_webid, filter=None)
    
    def get_one_by_webid(self, webid: WebId, 
                        target_type: ObjEnum | None = None)->SingleOutput:  
        self.ev_handler.fire_event(webid, target_type, name = 'pre_read_one',)
        obj: Obj = self._get_one(webid=webid)
        self.ev_handler.fire_event((obj,), name = 'pos_read_one',)
        if target_type is not None:
            # FAZER CAST PARA Obj especifico de pydantic
            check_obj_type(obj, target_type)
        
        return make_single_output(obj)

    def get_all_by_parentwebid_and_type(self, children_type: ObjEnum, 
                                        parent_webid: WebId, parent_type: ObjEnum | None = None)->ListOutput:
        """"""

        if parent_type is not None:
            parent_type.is_valid_child(children_type)
            parent = self._get_one(parent_webid)
            check_obj_type(parent, parent_type)
        
        objs: list[Obj] = self._get_all(parent_webid = parent_webid)
        
        return make_list_output(objs)
    
    def add_one_and_check_parent(self, parent_type: ObjEnum, webid: WebId, obj:Obj)->None:
        pass