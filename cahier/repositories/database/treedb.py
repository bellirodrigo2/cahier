# """ In Memory Database """
# from typing import Any
# from enum import Enum
# import json

# from pydantic import BaseModel
# from treelib import Tree

# from cahier.schemas.schemas import WebId, ObjEnum, InputObj

# ################################################################################


# class Ops(Enum):
#     Create = 'create'
#     Update = 'update'
#     Patch = 'patch'
#     Delete = 'delete'


# def from_json(d: dict[str, Any]):
#     pass

# class TreeData(BaseModel):
#     obj_type: ObjEnum
#     data: InputObj
    
# class TreeDB:
    
#     def __init__(self, tree: Tree) -> None:
#         self.__tree = tree
        
#     def add()