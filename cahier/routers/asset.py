""" Routers for Cahier Builder """

from typing import Annotated

from cahier.interfaces.asset import AssetServiceInterface
from cahier.schemas.objects import ObjEnum
from cahier.schemas.schemas import ListOutput, ObjInput, SingleOutput, WebId
from cahier.services.dependecy_injection import get_asset_service
from fastapi import APIRouter, Body, Depends, Path, Query, Request

###############################################################################

router = APIRouter(tags=[i.name for i in ObjEnum])


@router.get("/{target}/{webid}", response_model=SingleOutput)
def read_one(
    service: AssetServiceInterface = Depends(get_asset_service),
    target: ObjEnum = Path(title="..."),
    webid: WebId = Path(title="..."),
    selectedFields: Annotated[str | None, Query()] = None,
):
    return service.get_one_by_webid(target_type=target, webid=webid)


@router.get("/{target}/{webid}/{children}")  # , response_model=SingleOutput)
def read_all(
    request: Request,
    service: AssetServiceInterface = Depends(get_asset_service),
    target: ObjEnum = Path(title="..."),
    children: ObjEnum = Path(title="..."),
    webid: WebId = Path(title="..."),
    # https://stackoverflow.com/questions/62279710/fastapi-variable-query-parameters
    fieldFilter: Annotated[list[str] | None, Query(...)] = None,
    fieldFilterLike: Annotated[list[str] | None, Query(...)] = None,
    searchFullHierarchy: Annotated[bool | None, Query(...)] = None,
    sortField: Annotated[str | None, Query(...)] = None,
    sortOrder: Annotated[str | None, Query(...)] = None,
    startIndex: Annotated[int | None, Query(...)] = None,
    maxCount: Annotated[int | None, Query(...)] = None,
    selectedFields: Annotated[str | None, Query(...)] = None,
):

    queries = dict(request.query_params)

    if "fieldFilterLike" in queries:
        queries["fieldFilterLike"] = fieldFilterLike

    if "fieldFilter" in queries:
        queries["fieldFilter"] = fieldFilter

    if "selectedFields" in queries:
        queries["selectedFields"] = selectedFields

    # set HEADERS for pagination
    # total objects ????  teria que saber i numero total de items
    # from
    # to

    return service.get_all_by_webid(
        parent=target, children=children, webid=webid, query_dict=queries
    )


@router.post("/{target}/{webid}/{children}")
def create_one(
    service: AssetServiceInterface = Depends(get_asset_service),
    target: ObjEnum = Path(title="..."),
    webid: WebId = Path(title="..."),
    children: ObjEnum = Path(title="..."),
    obj: ObjInput = Body(title="Node JSON object to be added to the provided webid"),
):
    service.add_one(parent=target, webid=webid, children=children, obj=obj)
    # set header
    # set status_code
