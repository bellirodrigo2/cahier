""""""
from typing import Callable, Tuple

from ..interfaces import RepositoryInterface
from ..interfaces import AssetServiceInterface

from ..schemas import ObjEnum, map_type_to_parent
from ..schemas import WebId, Obj, ObjInput, SingleOutput, ListOutput
from ..schemas import  make_single_output, make_list_output
from ..schemas import check_obj_hierarchy

################################################################################

class AssetService:
    """"""
    
    def __init__(self,
            get_repo: Callable[[], RepositoryInterface],
            pre_proc: Callable[[], AssetServiceInterface] | None = None,
            post_proc: Callable[[frozenset[Obj]], AssetServiceInterface] | None = None,
        ) -> None:
        self.__pre_proc = pre_proc
        self.__get_repo = get_repo
        self.__post_proc = post_proc
    
    def _get_one(self, webid: WebId)->Obj:
        repo: RepositoryInterface = self.__get_repo()
        return repo.get_one_by_webid(webid=webid)
    
    def _get_all(self, parent_webid: WebId)->list[Obj]:
        repo: RepositoryInterface = self.__get_repo()
        return repo.get_all_by_parent_webid(webid=parent_webid, filter=None) #aqui entra os queries param
    
    
    def get_one_by_webid(self, webid: WebId, target_type: ObjEnum | None = None)->SingleOutput:  
        
        if self.__pre_proc:
            self.__pre_proc().get_one_by_webid(webid=webid, target_type=target_type)
        
        obj: Obj = self._get_one(webid=webid)
        
        if target_type is not None:
            # FAZER CAST PARA Obj especifico de pydantic
            check_obj_type(obj, target_type)
        
        if self.__post_proc:
            post_service: AssetServiceInterface = self.__post_proc(frozenset([obj]))
            post_service.get_one_by_webid(webid, target_type)
        
        return make_single_output(obj)


    def get_all_by_parentwebid_and_type(self, children_type: ObjEnum, parent_webid: WebId, parent_type: ObjEnum | None = None)->ListOutput:
        """"""

        if parent_type is not None:
            parent_type.is_valid_child(children_type)
            parent = self._get_one(parent_webid)
            check_obj_type(parent, parent_type)
        
        if self.__pre_proc:            
            self.__pre_proc().get_all_by_parentwebid_and_type(children_type, parent_webid, parent_type)
        
        objs: list[Obj] = self._get_all(parent_webid = parent_webid)
        
        if self.__post_proc:    
            post_service: AssetServiceInterface = self.__post_proc(frozenset(objs))
            post_service.get_all_by_parentwebid_and_type(children_type, parent_webid, parent_type)
        
        return make_list_output(objs)
    
    
    def add_one_and_check_parent(self, parent_type: ObjEnum, webid: WebId, obj:ObjInput)->None:
        pass