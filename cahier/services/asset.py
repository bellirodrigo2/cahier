""""""

from typing import Any, Callable

from cahier.interfaces.crud import CRUDInterface, ReadAllOptions
# from cahier.schemas.schema import (ListOutput, Obj, ObjInput, SingleOutput,
                                    # WebId)

from cahier.schemas.schemas import ObjEnum, WebId, is_valid_parent
from cahier.schemas.schemas import SingleOutput, ListOutput, BaseOutput, BaseInputObj

###############################################################################

def make_list_output():
    pass
def make_single_output():
    pass
class AssetServiceError(Exception):
    pass

def check_hierarchy(parent: ObjEnum, children: ObjEnum):
    if is_valid_parent(parent, children)
        err = f"Object type {parent=} can not has a child of type {children}"
        raise AssetServiceError(err)


class AssetService:
    """"""

    def __init__(
        self,
        get_repo: Callable[[], CRUDInterface],
    ) -> None:
        self.__get_repo = get_repo

    def _add_one(self, webid: WebId, obj: ObjInput) -> None:
        repo: CRUDInterface = self.__get_repo()
        repo.add_one(webid=webid, obj=obj)

    def _get_one(self, webid: WebId) -> Obj:
        repo: CRUDInterface = self.__get_repo()
        return repo.get_one_by_webid(webid=webid)

    def _get_all(
        self, webid: WebId, child: ObjEnum, query_opt: ReadAllOptions
    ) -> list[Obj]:
        repo: CRUDInterface = self.__get_repo()
        return repo.get_all_by_parent_webid(
            webid=webid, child=child, query_opt=query_opt
        )

    def read(self, webid: WebId, target: ObjEnum) -> SingleOutput:

        obj: BaseOutput = self._get_one(webid=webid)

        # if attributes is not a valid dict for the target Pydantic model,
        # an ValidationError is raised
        target.make(obj.attributes)

        return make_single_output(target, obj)

    def list(
        self,
        parent: ObjEnum,
        children: ObjEnum,
        webid: WebId,
        query_dict: ReadAllOptions,
    ) -> ListOutput:
        """"""

        check_hierarchy(parent, children)

        # CAST/ERROR CHECK
        # if parent_obj is not same model as parent, ValidationError is raised
        parent_obj = self._get_one(webid)
        parent.make(parent_obj.attributes)

        query_opt = ReadAllOptions(**query_dict)
        objs: list[BaseOutput] = self._get_all(
            webid=webid, child=children, query_opt=query_opt
        )

        return make_list_output(objs)

    def create(self, parent: ObjEnum, children: ObjEnum, webid: WebId, 
               obj: BaseInputObj) -> None:

        check_hierarchy(parent, children)
