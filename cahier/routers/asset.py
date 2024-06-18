""" Routers for Cahier Builder """
from typing import Annotated

from fastapi import APIRouter, Depends, Response, Path, Body, Query, Request

from ..interfaces import AssetServiceInterface
from ..schemas import WebId, ObjInput, SingleOutput, ListOutput, ObjEnum

from  ..config.depinj import make_asset_service

################################################################################

router = APIRouter(
    tags=[i.name for i in ObjEnum]
)

@router.get('/{target}/{webid}', response_model=SingleOutput)
def read_one(
    service: AssetServiceInterface = Depends(make_asset_service),
    target: ObjEnum = Path(title='...'),
    webid: WebId = Path(title='...'),
    selectedFields: Annotated[str | None, Query()] = None,
):
    return service.get_one_by_webid(target_type=target, webid=webid)

def check_path(target: ObjEnum, children: ObjEnum):
    pass

@router.get('/{target}/{parent_webid}/{children}', response_model=SingleOutput, 
            dependencies=[Depends(check_path)])
def read_all(
    req:Request,
    service: AssetServiceInterface = Depends(make_asset_service),
    target: ObjEnum = Path(title='...'),
    children: ObjEnum = Path(title='...'),
    parent_webid: WebId = Path(title='...'),
    fieldFilter: list[str] | None = Query(title='...', description=' filter field equal to value. use {Field:Target}. ex: Name:TargetName or Id:123456'), 
    fieldFilterLike: list[str] | None = Query(title='...', description=' same as fieldFilter, but field has (target), instead of equal (like SQL "LIKE" keyword)'),
    metadata: list[str] | None = Query(title='...'), #fazer apenas tem ou nao o campo do metadata aqui ???? e fazer mais elaborado nos views ????
    templateName: str | None = Query(title='...'),
    searchFullHierarchy: bool | None = Query('...'),
    sortField: str | None = Query(title='...', description='Field used to sort. Sorting order can be provided: {Field.Sorting} Options: Asc/Desc'),
    startIndex: int | None = Query(),
    maxCount: int | None = Query(),
    selectedFields: str | None = Query()
    
):
    req.query_params
    
    return service.get_all_by_parentwebid_and_type(parent_type=target, children_type=children, parent_webid=parent_webid)

@router.post('/{target}/{parent_webid}/{children}',
            dependencies=[Depends(check_path)])
def create_one(
    service: AssetServiceInterface = Depends(make_asset_service),
    target: ObjEnum = Path(title='...'),
    parent_webid: WebId = Path(title='...'),
    children: ObjEnum = Path(title='...'),
    obj: ObjInput = Body(title='Node JSON object to be added to the provided webids'),
):
    service.add_one_and_check_parent(parent_type=target, parent_webid=parent_webid, obj=obj)
    #set header
    #return code