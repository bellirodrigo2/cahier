""" In Memory Database """
from typing import Any
from enum import Enum

from pydantic import BaseModel
from treelib import Tree

from cahier.schemas.webid import WebId

################################################################################

class Ops(Enum):
    Create = 'create'
    Update = 'update'
    Patch = 'patch'
    Delete = 'delete'

class TreeOperation(BaseModel):
    
    operation: Ops
    target_webid: WebId
    value: dict[str, Any]

class TreeSession:
    
    def __init__(self, filename: str) -> None:
        # carregar a tree do file aqui
        self.__tree = Tree()
    
    def __call__(self):
        return self.__tree
    
    def close(self):
        # persist data here
        pass
    


def bootstrap(filename: str, **kwargs)->TreeSession:
    return TreeSession(filename=filename)


def get_memory_db(tree_session: TreeSession):
    """ """
    try:
        yield tree_session
    finally:
        tree_session.close()
