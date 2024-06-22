""""""

from abc import abstractmethod
from typing import Protocol

from cahier.schemas.objects import ObjEnum, ReadAllOptions
from cahier.schemas.schemas import Obj, WebId

################################################################################


class RepositoryInterface(Protocol):

    @staticmethod
    @abstractmethod
    def bootstrap(cls) -> None:
        pass

    def get_one_by_webid(self, webid: WebId) -> Obj:
        pass

    def get_all_by_parent_webid(
        self, child: ObjEnum, webid: WebId, query_opt: ReadAllOptions
    ) -> list[Obj]:
        pass

    def add_one(self, webid: WebId, obj: Obj) -> None:
        pass
