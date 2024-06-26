""" In Memory Repository """

from typing import Callable

from treelib import Tree

from cahier.interfaces.assetdao import ReadAllOptions, JsonReponse
from cahier.schemas.schemas import InputObj, Obj, ObjEnum, WebId

################################################################################


class InMemoryRepository:

    def __init__(self, get_db: Callable[[], Tree]) -> None:
        self.get_db = get_db

    def read(self, 
             webid: WebId, target_type: ObjEnum, options, ReadOptions
            ) -> JsonReponse:

        tree = self.get_db()
        node = tree.get_node(webid)
        if node:
            # checar se type do node = target_type
            return node.data
        raise Exception()

    def list(
        self,
        parent: ObjEnum,
        children: ObjEnum,
        webid: WebId,
        options: ReadAllOptions,
    ) -> list[JsonReponse] | JsonReponse:

        """"""
        tree = self.get_db()
        node = tree.get_node(webid)
        if node:
            # checar se type do node = target_type
            return node.children  # ... filtrar os types de children
    def create(
        self, parent: ObjEnum, children: ObjEnum, webid: WebId, obj: InputObj
    ) -> None:
        """"""

        tree = self.get_db()
        obj_ = Obj(obj)
        tree.create_node(tag=obj_.name, identifier=obj_.webid, data=obj_)
