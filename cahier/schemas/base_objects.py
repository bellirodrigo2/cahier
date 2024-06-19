""" Base Objects and hierarchies """
from enum import Enum
from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

################################################################################

class BaseType(Enum):
    server = None
    root = ['server']
    element = ['root']
    node = ['root', 'node']
    item = ['node', 'item']


map_base_to_parent = {i.name: i.value for i in BaseType}

class _BaseObj(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def obj_type(cls)->str:
        pass
    @classmethod
    @abstractmethod
    def base_type(cls)->BaseType:
        pass

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