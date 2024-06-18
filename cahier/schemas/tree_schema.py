""" """
from typing import Annotated
from enum import Enum, auto

from pydantic import Field

from . import NodeObj, ItemObj
from . import Obj


################################################################################

# OMO FAZER A DISTINÇÃO DE obj, objinput, objoutput ??????????????

class TreeNode(Obj):
    
    path: Annotated[str, Field(
        alias='Path',
        serialization_alias='Path',
    )]

class Node(NodeObj, TreeNode):
    
    template: Annotated[str, Field(
        alias='Template',
        serialization_alias='Template',
        default=''
    )]

class DataTypeEnum(Enum):
    string = auto()
    float = auto()
    int = auto()
    boolean = auto()
    byte = auto()
    timestamp = auto()

class Item(ItemObj, TreeNode):
    
    data_type: Annotated[DataTypeEnum, Field(
        alias='DataType',
        serialization_alias='DataType'
    )]
    
    data_source: Annotated[str, Field(
        alias='DataSource',
        serialization_alias='DataSource',
    )]