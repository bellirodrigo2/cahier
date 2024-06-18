""" Base Objects and hierarchies """
from enum import Enum

from .base_objects import _ServerObj, _BaseObj, _ElementObj, _ItemObj, _NodeObj, _RootObj
from .base_objects import map_base_to_parent

################################################################################


class DataServerObj(_ServerObj):
    @classmethod
    def obj_type(cls)->str:
        return 'dataserver'
class AssetServerObj(_ServerObj):
    @classmethod
    def obj_type(cls)->str:
        return 'assetserver'


class DataBaseObj(_RootObj):
    @classmethod
    def obj_type(cls)->str:
        return 'database'
class UserObj(_RootObj):
    @classmethod
    def obj_type(cls)->str:
        return 'user'


class ViewObj(_ElementObj):
    @classmethod
    def obj_type(cls)->str:
        return 'view'
class ProcObj(_ElementObj):
    @classmethod
    def obj_type(cls)->str:
        return 'proc'
class CollectionsObj(_ElementObj):
    @classmethod
    def obj_type(cls)->str:
        return 'collections'
class EnumSetObj(_ElementObj):
    @classmethod
    def obj_type(cls)->str:
        return 'enumset'
class KeyValueObj(_ElementObj):
    @classmethod
    def obj_type(cls)->str:
        return 'keyvalue'
class CounterObj(_ElementObj):
    @classmethod
    def obj_type(cls)->str:
        return 'counter'


class NodeObj(_NodeObj):
    @classmethod
    def obj_type(cls)->str:
        return 'node'
# class TemplateNode(_NodeObj):
    # pass


class ItemObj(_ItemObj):
    @classmethod
    def obj_type(cls)->str:
        return 'item'

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
