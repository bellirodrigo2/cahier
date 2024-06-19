""""""
import pytest
from unittest.mock import Mock

from typing import Callable, Awaitable

from icecream import ic

from fastapi.testclient import TestClient
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response

from cahier.main import app
from cahier import make_asset_service

from cahier.schemas import ObjEnum

################################################################################

# mock_asset_service = Mock()

def override_make_asset_service():
    return make_asset_service
# def override_make_asset_service():
    # return MockAssetService()

app.dependency_overrides[make_asset_service] = override_make_asset_service

class PrintMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        ic(request.method, request.url.path, request.url.query)
    
        resp = await call_next(request)
        return resp

# app.add_middleware(PrintMiddleware)

client = TestClient(app)

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

@pytest.fixture
def setup_data():
    yield _OKS, _NO_OKS, _NO_EXIST


def setup_function():
    # ic('setup function')
    mock_asset_service.reset()
    pass

    
def teardown_function():
    # ic('teardown function')
    pass


def for_each_obj_type_one(paths, webids, expected_code):
    for obj in paths:
        for id in webids:
            response = client.get(f'/{obj}/{id}')
            assert response.status_code == expected_code
            mock_asset_service.assert_called_once()
            # resp = response.json()  
            # ic(resp)

def get_all_valid_objs():
    return [i.name for i in ObjEnum]
    
def test_getone_ok(setup_data):
    ok_webids, nok_webids, no_exist_webids = setup_data
    # ASSERT IF MOCKED get_one was called
    # for_each_obj_type_one(get_all_valid_objs(), ok_webids, 200)

    
def test_getone_not_webid_nok(setup_data):
    ok_webids, nok_webids, no_exist_webids = setup_data
    # ASSERT IF MOCKED get_one was not called
    # for_each_obj_type_one(get_all_valid_objs(), nok_webids, 422)


def test_getone_not_found_nok(setup_data):
    ok_webids, nok_webids, no_exist_webids = setup_data
        # ASSERT IF MOCKED get_one was called
        #****************************
    # for_each_obj_type_one(get_all_valid_objs(), no_exist_webids, 422)


def test_getone_path_nok(setup_data):
    ok_webids, nok_webids, on_exist_webids = setup_data
    # ASSERT IF MOCKED get_one was not called
    for_each_obj_type_one(['no','existent', 'path'], ok_webids, 422)
