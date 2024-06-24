""" In Memory Repository """
from typing import Callable

from treelib import Tree

from cahier.interfaces.crud import ReadAllOptions
from cahier.schemas.schemas import WebId
from cahier.schemas.schemas import ObjEnum, BaseOutput, BaseInputObj, ListOutput, BaseObj

################################################################################

class InMemoryRepository:

    def __init__(self, get_db: Callable[[], Tree]) -> None:
        self.get_db = get_db

    def read(self, webid: WebId, target_type: ObjEnum) -> BaseOutput:

        tree = self.get_db()
        node = tree.get_node(webid)
        if node:
            # checar se type do node = target_type
            return node.data
        raise Exception()
    
    def list(self, parent: ObjEnum, children: ObjEnum, webid: WebId, 
            query_dict: ReadAllOptions) -> list[BaseOutput] | ListOutput:
        """"""
        tree = self.get_db()
        node = tree.get_node(webid)
        if node:
            # checar se type do node = target_type
            return node.children #... filtrar os types de children

    def create(self, parent: ObjEnum, children: ObjEnum, webid: WebId, 
               obj: BaseInputObj) -> None:
        """"""
        
        tree = self.get_db()
        obj_ = BaseObj(obj)
        tree.create_node(tag=obj_.name, identifier=obj_.webid, data=obj_)
