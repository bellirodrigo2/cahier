""""""
import pytest
from unittest.mock import MagicMock
from uuid import UUID

from icecream import ic

from fastapi.testclient import TestClient

from cahier.main import app
from cahier.routers.asset import get_asset_service

from cahier.schemas.objects import ObjEnum

from starlette.middleware.base import BaseHTTPMiddleware

################################################################################

class PrintMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        ic(request.method, request.url.path, request.url.query)
    
        resp = await call_next(request)
        return resp
# app.add_middleware(PrintMiddleware)

# https://opensource.com/article/23/4/using-mocks-python
# https://aaronlelevier.github.io/python-unit-testing-with-magicmock/
mock_session = MagicMock()
mock_session.get_one_by_webid.return_value = {
    'Id': 'foobar',
    'Attributes': {}
}
mock_session.get_all_by_parentwebid.return_value = {
    'Id': 'foobar',
    'Attributes': {}
}
# mock_session.FUNCNAMEHERE.side_effect = []

def mock_get_user_name():
    return mock_session

def override_get_asset_service():
    try:
        yield mock_session
    finally:
        pass
    
app.dependency_overrides[get_asset_service] = override_get_asset_service

client = TestClient(app)

@pytest.fixture
def mock_asset_service():
    return mock_session

def setup_function():
    mock_session.reset_mock()

def test_getone_wrong_path(mock_asset_service):
    id = '1c8accd9-2e70-11ef-a48f-3024a9fbd4aa'
    path = 'noexistentpath'
    response = client.get(f'/{path}/{id}')
    assert response.status_code == 422
    mock_asset_service.get_one_by_webid.assert_not_called()
    mock_asset_service.get_all_by_webid.assert_not_called()

@pytest.mark.parametrize('id, path',[('1c8accd9-2e70-11ef-a48f-3024a9fbd4aa', oe) 
                                for oe in ObjEnum])
def test_getone_ok(id, path, mock_asset_service):
    
    response = client.get(f'/{path.name}/{id}')
    assert response.status_code == 200
    mock_asset_service.get_one_by_webid.assert_called_with(target_type=path, webid=UUID(id))
    mock_asset_service.get_all_by_webid.assert_not_called()
    
@pytest.mark.parametrize('id, path', [('NOUUID', oe) for oe in ObjEnum])
def test_getone_wrong_webid(id, path, mock_asset_service):
    
    response = client.get(f'/{path.name}/{id}')
    assert response.status_code == 422
    mock_asset_service.get_one_by_webid.assert_not_called()
    mock_asset_service.get_all_by_webid.assert_not_called()


@pytest.mark.parametrize('parent, child', [('noexist', 'item'), ('node', 'noexist')])
def test_getall_wrong_path(parent, child, mock_asset_service):
    id = '1c8accd9-2e70-11ef-a48f-3024a9fbd4aa'
    response = client.get(f'/{parent}/{id}/{child}')
    assert response.status_code == 422
    mock_asset_service.get_one_by_webid.assert_not_called()
    mock_asset_service.get_all_by_webid.assert_not_called()


@pytest.mark.parametrize('parent, child', [
    (ObjEnum.assetserver, ObjEnum.database),
    (ObjEnum.database, ObjEnum.node), (ObjEnum.database, ObjEnum.view),
    (ObjEnum.node, ObjEnum.item), (ObjEnum.item,ObjEnum.item), 
    ])
def test_getall_ok(parent, child, mock_asset_service):
    
    id = '1c8accd9-2e70-11ef-a48f-3024a9fbd4aa'

    queries = ''
    response = client.get(
        f'/{parent.name}/{id}/{child.name}?{queries}'
        )
    
    assert response.status_code == 200
    mock_asset_service.get_all_by_webid.assert_called_with(
        parent=parent, children = child, webid=UUID(id), query_dict={}
        )
    mock_asset_service.get_one_by_webid.assert_not_called()

@pytest.mark.parametrize('id', ['NOUUID'])
def test_getall_wrongWEBID(id, mock_asset_service):
    
    parent_path = ObjEnum.node
    child_parent = ObjEnum.item
    
    response = client.get(f'/{parent_path.name}/{id}/{child_parent.name}')
    
    assert response.status_code == 422
    mock_asset_service.get_all_by_webid.assert_not_called()
    mock_asset_service.get_one_by_webid.assert_not_called()

    
@pytest.mark.parametrize('id', ['1c8accd9-2e70-11ef-a48f-3024a9fbd4aa'])
def test_getall_ok_w_query_params(id, mock_asset_service):
    
    parent_path = ObjEnum.node
    child_parent = ObjEnum.item
    
    queries = f'fieldFilter=F1111&fieldFilter=F2222&selectedFields=selll'
    
    response = client.get(f'/{parent_path.name}/{id}/{child_parent.name}?{queries}')
    
    assert response.status_code == 200
    expected_query_dict = {
        'fieldFilter' : ['F1111', 'F2222'],
        'selectedFields' : 'selll'
    }
    mock_asset_service.get_all_by_webid.assert_called_with(
        parent=parent_path, children = child_parent, 
        webid=UUID(id), query_dict=expected_query_dict
        )
    mock_asset_service.get_one_by_webid.assert_not_called()
 
@pytest.mark.parametrize('id, body', 
                         [('1c8accd9-2e70-11ef-a48f-3024a9fbd4aa', oe) 
                            for oe in [
                                {}, {'Name' : 'foo','ClientId': 'bar'}
                            ]
                        ])
def test_addone_ok(id, body, mock_asset_service):   
    
    parent_path = ObjEnum.node
    child_parent = ObjEnum.item
    
    response = client.post(f'/{parent_path.name}/{id}/{child_parent.name}', 
                           json=body)
    assert response.status_code == 200
    
    mock_asset_service.get_one_by_webid.assert_not_called()
    mock_asset_service.get_all_by_webid.assert_not_called()
    mock_asset_service.add_one.assert_called_once()

@pytest.mark.parametrize('id', ['NOUUID'])
def test_addone_wrongWEBID(id, mock_asset_service):
    
    parent_path = ObjEnum.node
    child_parent = ObjEnum.item
    
    response = client.post(f'/{parent_path.name}/{id}/{child_parent.name}',
                           json={})
    
    assert response.status_code == 422
    mock_asset_service.get_all_by_webid.assert_not_called()
    mock_asset_service.get_one_by_webid.assert_not_called()
    mock_asset_service.add_one.assert_not_called()