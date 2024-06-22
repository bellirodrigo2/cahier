""" Base Objects and hierarchies """

from abc import ABC, abstractmethod

from pydantic import BaseModel

##############################################################################


class _BaseObj(BaseModel, ABC):
    @classmethod
    @abstractmethod
    def base_type(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def parent(cls) -> list[str]:
        pass


class _ServerObj(_BaseObj):
    @classmethod
    def base_type(cls) -> str:
        return "server"

    @classmethod
    def parent(cls) -> list[str]:
        return []


class _RootObj(_BaseObj):
    @classmethod
    def base_type(cls) -> str:
        return "root"

    @classmethod
    def parent(cls) -> list[str]:
        return ["server"]


class _ElementObj(_BaseObj):
    @classmethod
    def base_type(cls) -> str:
        return "element"

    @classmethod
    def parent(cls) -> list[str]:
        return ["root"]


class _NodeObj(_BaseObj):
    @classmethod
    def base_type(cls) -> str:
        return "node"

    @classmethod
    def parent(cls) -> list[str]:
        return ["root", "node"]


class _ItemObj(_BaseObj):
    @classmethod
    def base_type(cls) -> str:
        return "item"

    @classmethod
    def parent(cls) -> list[str]:
        return ["node", "item"]
