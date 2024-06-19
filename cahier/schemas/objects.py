""" Base Objects and hierarchies """
from typing import Annotated
from enum import Enum

from .timestamp import Timestamp
from .base_objects import _ServerObj, _BaseObj, _ElementObj, _ItemObj, _NodeObj, _RootObj
from .base_objects import map_base_to_parent, Field

################################################################################


class DataServer(_ServerObj):
    @classmethod
    def obj_type(cls)->str:
        return 'dataserver'
    
class AssetServer(_ServerObj):
    @classmethod
    def obj_type(cls)->str:
        return 'assetserver'


class DataBase(_RootObj):
    @classmethod
    def obj_type(cls)->str:
        return 'database'
class User(_RootObj):
    @classmethod
    def obj_type(cls)->str:
        return 'user'


class View(_ElementObj):
    @classmethod
    def obj_type(cls)->str:
        return 'view'
class Proc(_ElementObj):
    @classmethod
    def obj_type(cls)->str:
        return 'proc'
class Collections(_ElementObj):
    @classmethod
    def obj_type(cls)->str:
        return 'collections'
class EnumSet(_ElementObj):
    @classmethod
    def obj_type(cls)->str:
        return 'enumset'
class KeyValue(_ElementObj):
    @classmethod
    def obj_type(cls)->str:
        return 'keyvalue'
class Counter(_ElementObj):
    @classmethod
    def obj_type(cls)->str:
        return 'counter'

pathField = Annotated[str, Field(
        alias='Path',
        serialization_alias='Path',
    )]

class Node(_NodeObj):
    @classmethod
    def obj_type(cls)->str:
        return 'node'
    
    path: pathField
    
    template: Annotated[str, Field(
        alias='Template',
        serialization_alias='Template',
        default=''
    )]
class DataTypeEnum(Enum):
    string = str
    float = float
    int = int
    boolean = bool
    byte = bytes
    timestamp = Timestamp

class Item(_ItemObj):
    @classmethod
    def obj_type(cls)->str:
        return 'item'
    
    path: pathField
    
    data_type: Annotated[DataTypeEnum, Field(
        alias='DataType',
        serialization_alias='DataType'
    )]
    
    data_source: Annotated[str, Field(
        alias='DataSource',
        serialization_alias='DataSource',
    )]
################################################################################

# get all classes derived from _BaseObj
deriveds = [[c for c in cls.__subclasses__()] for cls in _BaseObj.__subclasses__()]
nested_classes = [item for sublist in deriveds for item in sublist]


# create a enum type from the derived classes
types_list = {x.obj_type(): x.obj_type() for x in nested_classes}

class CompareObjEnum:
    
    def is_valid_child(self, child):
        possible_parent = map_type_to_parent[child.value]
        if possible_parent and self.value in possible_parent:
            return
        raise TypeHierarchyError(parent_type=self, children_type=child)

ObjEnum = Enum(
    'ObjEnum',
    types_list,
    module='objects',
    qualname='objects.ObjEnum',
    type=CompareObjEnum
    )

#create map from obj type to base class and then to possible parent types
map_type_to_base = {c.obj_type():c.base_type().name for c in nested_classes}
map_type_to_parent = {k:map_base_to_parent[v] for k,v in map_type_to_base.items()}

class TypeHierarchyError(Exception):
    """ failure in the type hierarchy. parent and children types are incompatible """
    
    def __init__(self, parent_type: ObjEnum, children_type: ObjEnum):
        self.message = f'Type Hierarchy Error. \
            Object of type {parent_type=} can´t have a children of type {children_type=}'
        self.name = 'TypeHierarchyError'
