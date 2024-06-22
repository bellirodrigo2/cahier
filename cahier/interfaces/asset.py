""""""

from typing import Any, Protocol

from cahier.schemas.objects import ObjEnum
from cahier.schemas.schemas import ListOutput, ObjInput, SingleOutput, WebId

################################################################################


class AssetError(Exception):
    pass


class AssetServiceInterface(Protocol):

    def get_one_by_webid(
        self, webid: WebId, target_type: ObjEnum | None
    ) -> SingleOutput:
        """"""
        pass

    def get_all_by_webid(
        self,
        parent: ObjEnum,
        children: ObjEnum,
        webid: WebId,
        query_dict: dict[str, Any],
    ) -> ListOutput:
        """"""
        pass

    def add_one(
        self, parent: ObjEnum, children: ObjEnum, webid: WebId, obj: ObjInput
    ) -> None:
        """"""
        pass
