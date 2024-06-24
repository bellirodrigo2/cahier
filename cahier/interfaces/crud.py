""""""

from typing import Any, Protocol

from cahier.schemas.objects import ObjEnum, ReadAllOptions
from cahier.schemas.schemas import WebId, Obj, SingleOutput, ListOutput, ObjInput

################################################################################

SingleOutput inherit de Obj
obj inherit de ObjInput
listouput é compositiom com list[obj]

asset: SingleOutput, ListOutput, ObjInput
repository: Obj, list[Obj], Obj

class CRUDInterface(Protocol):

    def read(
        self, webid: WebId, target_type: ObjEnum | None
    ) -> Obj | SingleOutput:
        """"""
        pass

    def list(
        self,
        parent: ObjEnum,
        children: ObjEnum,
        webid: WebId,
        query_dict: ReadAllOptions,
    ) -> list[Obj] | ListOutput:
        """"""
        pass

    def create(
        self, parent: ObjEnum, children: ObjEnum, webid: WebId, obj: Obj |  ObjInput
    ) -> None:
        """"""
        pass
