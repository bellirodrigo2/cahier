""" Base Objects and hierarchies """

from abc import ABC, abstractmethod

from pydantic import BaseModel

##############################################################################


class BaseObj(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def base_type(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def parent(cls) -> list[str]:
        pass    
    @classmethod
    @abstractmethod
    def children(cls) -> list[str]:
        pass


class ServerObj(BaseObj):
    @classmethod
    def base_type(cls) -> str:
        return "server"

    @classmethod
    def parent(cls) -> list[str]:
        return []

    @classmethod
    def children(cls) -> list[str]:
        return  ['root']


class RootObj(BaseObj):
    @classmethod
    def base_type(cls) -> str:
        return "root"

    @classmethod
    def parent(cls) -> list[str]:
        return ["server"]

    @classmethod
    def children(cls) -> list[str]:
        return  ['element', 'node']

class ElementObj(BaseObj):
    @classmethod
    def base_type(cls) -> str:
        return "element"

    @classmethod
    def parent(cls) -> list[str]:
        return ["root"]

    @classmethod
    def children(cls) -> list[str]:
        return  []

class NodeObj(BaseObj):
    @classmethod
    def base_type(cls) -> str:
        return "node"

    @classmethod
    def parent(cls) -> list[str]:
        return ["root", "node"]

    @classmethod
    def children(cls) -> list[str]:
        return  ['node', 'item']

class ItemObj(BaseObj):
    @classmethod
    def base_type(cls) -> str:
        return "item"

    @classmethod
    def parent(cls) -> list[str]:
        return ["node", "item"]

    @classmethod
    def children(cls) -> list[str]:
        return  ['item']