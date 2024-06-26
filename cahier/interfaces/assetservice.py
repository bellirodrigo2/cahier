""""""

from typing import Any, Protocol

from cahier.schemas.schemas import InputObj, ObjEnum, WebId
from cahier.interfaces.auxdata import ReadAllOptions, JsonReponse

################################################################################


class AssetInterface(Protocol):

    def read(self, 
            target: ObjEnum,
            webid: WebId, 
            selected_fields: tuple[str] = None
            ) -> JsonReponse:
        """"""
        pass

    def list(
        self,
        parent: ObjEnum,
        children: ObjEnum,
        webid: WebId,
        options: ReadAllOptions,
    ) -> tuple[JsonReponse]:
        """"""
        pass

    def create(
        self, parent: ObjEnum, 
        children: ObjEnum, 
        webid: WebId, obj: InputObj
    ) -> WebId:
        """"""
        pass

if __name__ == '__main__':
    pass