""""""
from typing import Tuple, Callable, Any

from cahier.interfaces.asset import AssetServiceInterface
from cahier.interfaces.repository import RepositoryInterface, ReadAllOptions

from cahier.schemas.objects import ObjEnum
from cahier.schemas.schemas import WebId, Obj, SingleOutput, ListOutput, ObjInput

from cahier.schemas.factory import  make_single_output, make_list_output

from cahier.interfaces.events import EventHandlerInterface

################################################################################

class AssetServiceError(Exception):
    pass

def check_hierarchy(parent: ObjEnum, children: ObjEnum):
    if parent.parent_of(children) == False:
        err = f'Object type {parent=} can not has a child of type {children}'
        raise AssetServiceError(err)

class AssetService:
    """"""

    event_handlers: dict[str, Callable[..., None]] = {}
    
    def __init__(self,
            get_repo: Callable[[], RepositoryInterface],
            ev_handler: Callable[[], EventHandlerInterface] | None,
        ) -> None:
        self.__get_repo = get_repo
        self.ev_handler = ev_handler
    
    def add_event_handler(self, event_name: str, callback: Callable[..., None])->None:
        if self.ev_handler:
            self.ev_handler().add_event_handler(event_name=event_name, callback=callback)
    
    def remove_event_handler(self, event_name: str,)->None:
        if self.ev_handler:
            self.ev_handler().remove_event_handler(event_name=event_name)
    
    def _add_one(self, webid: WebId, obj: ObjInput)->None:
        repo: RepositoryInterface = self.__get_repo()
        repo.add_one(webid=webid, obj=obj)
    
    
    def _get_one(self, webid: WebId)->Obj:
        repo: RepositoryInterface = self.__get_repo()
        return repo.get_one_by_webid(webid=webid)
    
    def _get_all(self, webid: WebId, child: ObjEnum, query_opt: ReadAllOptions)->list[Obj]:
        repo: RepositoryInterface = self.__get_repo()
        return repo.get_all_by_parent_webid(webid=webid, child=child, query_opt=query_opt)
    
    def get_one_by_webid(self, webid: WebId, target: ObjEnum)->SingleOutput:  
        
        if self.ev_handler:
            self.ev_handler().fire_event(
                name = 'pre_read_one', webid=webid, target=target,
                )
       
        obj: Obj = self._get_one(webid=webid)
        
        if self.ev_handler:
            self.ev_handler().fire_event(name = 'pos_read_one', obj=(obj,),)
        
        # CAST/ERROR CHECK
        # if attributes is not a valid dict for the target Pydantic model, 
        # an ValidationError is raised 
        target.make(obj.attributes)
        
        return make_single_output(target, obj)

    def get_all_by_webid(self, parent: ObjEnum, children: ObjEnum,
                                webid: WebId, query_dict: dict[str, Any]
                                )->ListOutput:
        """"""

        check_hierarchy(parent, children)
        
        # CAST/ERROR CHECK
        # if parent_obj is not same model as parent, an ValidationError is raised 
        parent_obj = self._get_one(webid)
        parent.make(parent_obj.attributes) 
        
        query_opt = ReadAllOptions(**query_dict)
        objs: list[Obj] = self._get_all(webid = webid, child=children, query_opt=query_opt)
        
        return make_list_output(objs)
    
    def add_one(self, 
                    parent: ObjEnum, children: ObjEnum, webid: WebId, obj:ObjInput
                )->None:
        
        check_hierarchy(parent, children)
        