""" Base Objects and hierarchies """
from enum import Enum
from abc import ABC, abstractmethod

################################################################################

class BaseType(Enum):
    server = None
    root = ['server']
    element = ['root']
    node = ['root', 'node']
    item = ['node', 'item']


map_base_to_parent = {i.name: i.value for i in BaseType}


class _BaseObj(ABC):
    @classmethod
    @abstractmethod
    def obj_type(cls)->str:
        pass
        # return cls.__name__.lower()
    @classmethod
    @abstractmethod
    def base_type(cls)->BaseType:
        pass
    # @classmethod
    # def base_name(cls)->str:
    #     return cls.base_type().name


class _ServerObj(_BaseObj):
    @classmethod
    def base_type(cls)->BaseType:
        return BaseType.server


class _RootObj(_BaseObj):
    @classmethod
    def base_type(cls)->BaseType:
        return BaseType.root


class _ElementObj(_BaseObj):
    @classmethod
    def base_type(cls)->BaseType:
        return BaseType.element


class _NodeObj(_BaseObj):
    @classmethod
    def base_type(cls)->BaseType:
        return BaseType.node


class _ItemObj(_BaseObj):
    @classmethod
    def base_type(cls)->BaseType:
        return BaseType.item