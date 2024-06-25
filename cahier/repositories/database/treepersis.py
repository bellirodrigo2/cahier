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
    obj_type: ObjEnum | None = None
    obj: Obj | None = None
    
# precisa de patch ?????

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
        
        #append all the operations to file
        pass

class ObjNotFound(Exception):
    pass

class TreePersis:
    
    def __init__(self, tree: Tree, logger: OpLogger) -> None:
        self.__tree = tree
        self.__logger = logger
        
    def to_json(self):
        return self.__tree.to_json(with_data=True)    
        
    def get_node(self, webid: WebId)-> Obj:
        node = self.__tree.get_node(webid)
        if node:
            return node.data
        raise ObjNotFound()
        
    def add_node(self, type: ObjEnum, obj: Obj)-> None:
        """"""
        self.__tree.create_node(tag=obj.name, identifier=obj.webid, data=obj)
        op =  TreeOperation(
                TreeOpEnum.Create, target=obj.webid, obj_type=type, obj=obj
            )
        self.__logger.push(op)

    def update_operation(self, webid: WebId, update_object: UpdateObj)-> None:
        
        obj: Obj = self.get_node(webid=webid)
        #testa se o type esta correto ou nao ???? nao deveria
        
        #atualizar o OBJETO &******************************
        op = TreeOperation(
            operation=TreeOpEnum.Update, target=webid, obj=update_object
        )
        self.__logger.push(op)
        
#**************update e patch repete inicio da função e fim... injetar função para update x patch

    def patch_operation(self, webid: WebId, update_object: UpdateObj)-> None:
        obj: Obj = self.get_node(webid=webid)
        #testa se o type esta correto ou nao ???? nao deveria
        
        #atualizar o OBJETO &******************************
        op = TreeOperation(
            operation=TreeOpEnum.Update, target=webid, obj=update_object
        )
        self.__logger.push(op)

    def delete_operation(self, webid: WebId)-> None:
        self.__tree.remove_node(identifier=webid)
        op =  TreeOperation(
                TreeOpEnum.Delete, target=webid'
            )
        self.__logger.push(op)