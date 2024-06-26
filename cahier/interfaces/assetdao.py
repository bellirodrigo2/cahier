""""""

from typing import Any, Protocol

from cahier.schemas.schemas import Obj, ObjEnum, WebId
from cahier.interfaces.auxdata import ReadAllOptions, JsonReponse

################################################################################

class AssetDAOInterface(Protocol):

    def read(self, 
            webid: WebId, 
            selected_fields: tuple[str] | None = None
            ) -> JsonReponse:
        """"""
        pass

    def list(
        self,
        children: ObjEnum,
        webid: WebId,
        options: ReadAllOptions,
    ) -> tuple[JsonReponse]:
        """"""
        pass

    def create(
        self, 
        webid: WebId, 
        obj: Obj
    ) -> WebId:
        """"""
        pass

if __name__ == '__main__':
    pass