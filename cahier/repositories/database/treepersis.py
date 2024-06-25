""" Tree Persistence """
from enum import Enum
from typing import Protocol

from treelib import Tree

from pydantic import BaseModel

from cahier.schemas.schemas import ObjEnum, Obj, UpdateObj
from cahier.schemas.webid import WebId

################################################################################

class TreeOpEnum(Enum):
    Create = 'create'
    Update = 'update'
    Patch = 'patch'
    Delete = 'delete'
    
class TreeOperation(BaseModel):
    operation: TreeOpEnum
    target: WebId
    obj_type: ObjEnum
    obj: Obj
    
# fazer um logger
# precisa de patch ?????
# ja escrever no file ???? acho que sim... fazer classe entao ?
# fazer decorator para a Tree() ????

class OpLogger(Protocol):
    
    def push(self, op: TreeOperation):
        pass
    
    def flush(self, filename: str | None):
        pass

class FileLogger:
    
    def __init__(self, 
                filename: str, num_flush: int, logger: list[TreeOperation]
                ) -> None:
        self.__filename = filename
        self.__num_flush = num_flush
        self.__logger = logger

    def push(self, op: TreeOperation):
        
        self.__logger.append(op)
        self._check_flush()
    
    def _check_flush(self, filename: str | None):
        
        file = filename or self.__filename
        if len(self.__logger) > self.__num_flush:
            self.flush()
            
    def flush(self, filename: str | None):
        pass

class TreePersis:
    
    def __init__(self, tree: Tree, logger: OpLogger) -> None:
        self.__tree = tree
        self.__logger = logger
        
    def to_json(self):
        return self.__tree.to_json(with_data=True)    
        
    def get_node(self, webid: WebId):
        return self.__tree.get_node(webid)
        
    def add_node(self, type: ObjEnum, obj: Obj):
        """"""
        self.__tree.create_node(tag=obj.name, identifier=obj.webid, data=obj)
        op =  TreeOperation(
                TreeOpEnum.create, target=obj.webid, obj_type=type, obj=obj
            )
        self.__logger.push()

    def update_operation(
        self, webid: WebId, update_object: UpdateObj
    ):
        pass

    def patch_operation(self, webid: WebId, update_object: UpdateObj):
        pass

    def delete_operation(self, webid: WebId):
        pass