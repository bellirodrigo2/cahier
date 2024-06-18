""""""
from icecream import ic

from cahier.schemas import WebId, Obj, ObjInput, ObjEnum, SingleOutput, ListOutput, Attribute

from cahier.interfaces import AssetNotFoundError

################################################################################

class MockAssetService:
    
    _OKS = [
        '64ac464e-2cc6-11ef-b37b-3024a9fbd4aa',
        '64ac4651-2cc6-11ef-8f5c-3024a9fbd4aa',
        '64ac4652-2cc6-11ef-bc05-3024a9fbd4aa',
    ]
    
    _NO_OKS = [
        'foo',
        '64ac650-2cc6-11ef-af53-3024a9fbd4aa',
        '64ac652-2cc6-11ef-bc05-3024a9fbd4aa',        
    ]
    
    _NO_EXIST = [
        'cb6fe5ca-2ccd-11ef-a817-3024a9fbd4aa'
        'cb6fe5cb-2ccd-11ef-be39-3024a9fbd4aa'
        'cb6fe5cc-2ccd-11ef-a9db-3024a9fbd4aa'
    ]
    
    def get_one_by_webid(self, webid: WebId, target_type: ObjEnum | None = None)->SingleOutput:
        ic('MOCKED get_one', webid, target_type)
        
        if str(webid) in MockAssetService._NO_EXIST:
            raise AssetNotFoundError()
        return SingleOutput(client_id='fooid', attributes=Attribute(), obj_type='item')

    def get_all_by_parentwebid_and_type(self, children_type: ObjEnum, parent_webid: WebId, parent_type: ObjEnum | None = None)->ListOutput:
        ic(parent_type, children_type, parent_webid)
        return
    
    def add_one_and_check_parent(self, parent_type: ObjEnum, webid: WebId, obj:ObjInput)->None:
        ic(parent_type, webid, obj)
        return