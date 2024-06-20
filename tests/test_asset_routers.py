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

def test_getone_ok(mock_asset_service):
    id = '1c8accd9-2e70-11ef-a48f-3024a9fbd4aa'
    path = ObjEnum.node
    response = client.get(f'/{path.name}/{id}')
    assert response.status_code == 200
    mock_asset_service.get_one_by_webid.assert_called_with(target_type=path, webid=UUID(id))

def test_getone_wrong_path(mock_asset_service):
    id = '1c8accd9-2e70-11ef-a48f-3024a9fbd4aa'
    path = lambda: None
    path.name = 'noexistentpath'
    response = client.get(f'/{path.name}/{id}')
    assert response.status_code == 422
    mock_asset_service.get_one_by_webid.assert_not_called()
    
def test_getone_wrong_webid(mock_asset_service):
    id = 'foo'
    path = ObjEnum.node
    response = client.get(f'/{path.name}/{id}')
    assert response.status_code == 422
    mock_asset_service.get_one_by_webid.assert_not_called()
    
    # test all possible paths to read_one
    # test all possible paths to read_all
    
    #test raise exception on event_handler (mock it out!)