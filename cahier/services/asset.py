""""""

from typing import Any, Callable

from cahier.interfaces.crud import CRUDInterface, ReadOptions, JsonReponse
from cahier.schemas.schemas import InputObj, Obj, ObjEnum, WebId, is_valid_parent

###############################################################################



class AssetServiceError(Exception):
    pass


def check_hierarchy(parent: ObjEnum, children: ObjEnum):
    if is_valid_parent(parent, children) is False:
        err = f"Object type {parent=} can not has a child of type {children}"
        raise AssetServiceError(err)

def filter_response(obj: Obj, selected_fields: list[str] | None)-> JsonReponse:
    return {field : obj[field] for field in selected_fields if field in obj} \
        if selected_fields else obj

def add_link(filtered: JsonReponse, target: ObjEnum)->JsonReponse:
    filtered['Links'] = []
    return filtered

class AssetService:
    """"""

    def __init__(
        self,
        get_repo: Callable[[], CRUDInterface],
    ) -> None:
        self.__get_repo = get_repo

    def _add_one(self, webid: WebId, obj: InputObj) -> WebId:
        repo: CRUDInterface = self.__get_repo()
        return repo.create(webid=webid, obj=obj)

    def _get_one(self, webid: WebId) -> JsonReponse:
        repo: CRUDInterface = self.__get_repo()
        return repo.read(webid=webid)

    def _get_all(
        self, webid: WebId, child: ObjEnum, options: ReadOptions | None
    ) -> list[Obj]:
        repo: CRUDInterface = self.__get_repo()
        return repo.list(webid=webid, child=child, options=options)
    
    def read(self, 
             webid: WebId, target: ObjEnum, options: ReadOptions | None = None
            ) -> JsonReponse:
        
        obj: JsonReponse = self._get_one(webid=webid)
        # if attributes is not a valid dict for the target Pydantic model,
        # an ValidationError is raised
        target.make(obj)

        filtered = filter_response(obj, options.selected_fields) if options else obj
        return add_link(filtered, target)

    def list(
        self,
        parent: ObjEnum,
        children: ObjEnum,
        webid: WebId,
        options: ReadOptions,
    ) -> list[JsonReponse]:
        """"""

        check_hierarchy(parent, children)

        # CAST/ERROR CHECK
        # if parent_obj is not same model as parent, ValidationError is raised
        ######## **** SE O ID TIVER INFO DE TYPE, ESSE GET NAO PRECISA (um query a menos)
        parent_obj = self._get_one(webid)
        parent.make(parent_obj)

        #if parent/children is valid, and parent obj is the rigth type, 
        # the _get_all() results type should be consistent
        objs: list[JsonReponse] = self._get_all(
            webid=webid, child=children, options=options
        )
        
        filtereds = [filter_response(obj, options.selected_fields) for obj in objs] if options else objs
        
        return add_link(filtereds, children)

        return make_list_output(objs)

    def create(
        self, parent: ObjEnum, children: ObjEnum, webid: WebId, obj: InputObj
    ) -> WebId:

        check_hierarchy(parent, children)
        
        # CAST/ERROR CHECK
        # if obj is not same model as children, ValidationError is raised
        children.make(obj)
        
        return self._add_one(webid=webid, obj=obj)

if __name__ == '__main__':
    
    obj1 = {
        'Name': 'cfweqwwq',
        'Descr': 'xxxxxxxx',
        'Age': 45,
        'isOK': True,
    }
    
    selected = ['Name']
    assert 'Name' in filter_response(obj1, selected)
    assert 'Descr' not in filter_response(obj1, selected)
    assert 'Age' not in filter_response(obj1, selected)
    assert 'isOK' not in filter_response(obj1, selected)
    selected.append('Age')
    assert 'Name' in filter_response(obj1, selected)
    assert 'Descr' not in filter_response(obj1, selected)
    assert 'Age' in filter_response(obj1, selected)
    assert 'isOK' not in filter_response(obj1, selected)
    selected.append('Descr')
    assert 'Name' in filter_response(obj1, selected)
    assert 'Descr' in filter_response(obj1, selected)
    assert 'Age' in filter_response(obj1, selected)
    assert 'isOK' not in filter_response(obj1, selected)
    selected.append('isOK')
    assert 'Name' in filter_response(obj1, selected)
    assert 'Descr' in filter_response(obj1, selected)
    assert 'Age' in filter_response(obj1, selected)
    assert 'isOK' in filter_response(obj1, selected)
    selected.append('NOEXISTENTFIELD')
    assert 'Name' in filter_response(obj1, selected)
    assert 'Descr' in filter_response(obj1, selected)
    assert 'Age' in filter_response(obj1, selected)
    assert 'isOK' in filter_response(obj1, selected)
    selected = {}
    assert len(filter_response(obj1, selected)) == 0