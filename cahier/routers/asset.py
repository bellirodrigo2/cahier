""" Routers for Cahier Builder """

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query, Request

from cahier.interfaces.crud import CRUDInterface, ReadAllOptions
from cahier.schemas.schemas import ObjEnum, ListOutput, BaseInputObj, SingleOutput, WebId
from cahier.services.dependecy_injection import make_asset

###############################################################################

router = APIRouter(tags=[i.name for i in ObjEnum])


@router.get("/{target}/{webid}", response_model=SingleOutput)
def read_one(
    service: CRUDInterface = Depends(make_asset),
    target: ObjEnum = Path(title="..."),
    webid: WebId = Path(title="..."),
    selectedFields: Annotated[str | None, Query()] = None,
):
    return service.read(target_type=target, webid=webid)


@router.get("/{target}/{webid}/{children}")  # , response_model=SingleOutput)
def read_all(
    request: Request,
    service: CRUDInterface = Depends(make_asset),
    target: ObjEnum = Path(title="..."),
    children: ObjEnum = Path(title="..."),
    webid: WebId = Path(title="..."),
    # https://stackoverflow.com/questions/62279710/fastapi-variable-query-parameters
    field_filter: Annotated[list[str] | None, Query(...)] = None,
    field_filter_like: Annotated[list[str] | None, Query(...)] = None,
    search_full_hierarchy: Annotated[bool | None, Query(...)] = None,
    sort_field: Annotated[str | None, Query(...)] = None,
    sort_order: Annotated[str | None, Query(...)] = None,
    start_index: Annotated[int | None, Query(...)] = None,
    max_count: Annotated[int | None, Query(...)] = None,
    selected_fields: Annotated[list[str] | None, Query(...)] = None,
):

    queries = dict(request.query_params)

    if "field_filter" in queries:
        queries["field_filter"] = field_filter
        
    if "field_filter_like" in queries:
        queries["field_filter_like"] = field_filter_like


    if "selected_fields" in queries:
        queries["selected_fields"] = selected_fields

    return service.list(
        parent=target, children=children, webid=webid, 
        query_dict=ReadAllOptions(**queries)
    )


@router.post("/{target}/{webid}/{children}")
def create_one(
    service: CRUDInterface = Depends(make_asset),
    target: ObjEnum = Path(title="..."),
    webid: WebId = Path(title="..."),
    children: ObjEnum = Path(title="..."),
    obj: BaseInputObj = Body(title="Node JSON object to be added to the provided webid"),
):
    service.create(parent=target, webid=webid, children=children, obj=obj)
    # set header
    # set status_code