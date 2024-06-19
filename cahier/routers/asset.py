""" Routers for Cahier Builder """
from typing import Annotated, Tuple

from fastapi import APIRouter, Depends, Path, Body, Query

from cahier import AssetServiceInterface
from cahier import WebId, Obj, SingleOutput, ListOutput, ObjEnum

from cahier import get_fire_event, make_asset_service

################################################################################

router = APIRouter(
    tags=[i.name for i in ObjEnum]
)

@router.get('/{target}/{webid}', response_model=SingleOutput)
def read_one(
    service: AssetServiceInterface = Depends(make_asset_service),
    fire_event = Depends(get_fire_event),
    target: ObjEnum = Path(title='...'),
    webid: WebId = Path(title='...'),
    selectedFields: Annotated[str | None, Query()] = None,
):
    fire_event('pre_read_one', (target, webid))
    obj: Obj = service.get_one_by_webid(target_type=target, webid=webid)
    fire_event('post_read_one', (obj,))
    return obj

def check_path(target: ObjEnum, children: ObjEnum):
    pass

@router.get('/{target}/{parent_webid}/{children}', response_model=SingleOutput, 
            dependencies=[Depends(check_path)])
def read_all(
    service: AssetServiceInterface = Depends(make_asset_service),
    fire_event = Depends(get_fire_event),
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
    fire_event('pre_read_all', (target, parent_webid, children))
    objs: ListOutput = service.get_all_by_parentwebid_and_type(
        parent_type=target, children_type=children, parent_webid=parent_webid
        )
    fire_event('post_read_all', (objs))
    return objs

@router.post('/{target}/{parent_webid}/{children}',
            dependencies=[Depends(check_path)])
def create_one(
    service: AssetServiceInterface = Depends(make_asset_service),
    target: ObjEnum = Path(title='...'),
    parent_webid: WebId = Path(title='...'),
    children: ObjEnum = Path(title='...'),
    obj: Obj = Body(title='Node JSON object to be added to the provided webids'),
):
    service.add_one_and_check_parent(parent_type=target, parent_webid=parent_webid, obj=obj)
    #set header
    #return code