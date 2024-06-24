""""""

import pytest
from unittest.mock import MagicMock
from uuid import UUID, uuid1

from icecream import ic

from fastapi.testclient import TestClient

from cahier.main import app
from cahier.routers.asset import make_asset

from cahier.schemas.schemas import ObjEnum
from cahier.interfaces.crud import ReadAllOptions

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
mock_session.read.return_value = {"links": [], "client_id": 'foobar', "webid": uuid1()}
# mock_session.list.return_value = {"Name": "foobar"}
# mock_session.FUNCNAMEHERE.side_effect = []


def mock_get_user_name():
    return mock_session


def override_get_asset_service():
    try:
        yield mock_session
    finally:
        pass


app.dependency_overrides[make_asset] = override_get_asset_service

client = TestClient(app)


@pytest.fixture
def mock_asset_service():
    return mock_session


def setup_function():
    mock_session.reset_mock()


def test_getone_wrong_path(mock_asset_service):
    id = "1c8accd9-2e70-11ef-a48f-3024a9fbd4aa"
    path = "noexistentpath"
    response = client.get(f"/{path}/{id}")
    assert response.status_code == 422
    mock_asset_service.read.assert_not_called()
    mock_asset_service.list.assert_not_called()


@pytest.mark.parametrize(
    "id, path", [("1c8accd9-2e70-11ef-a48f-3024a9fbd4aa", oe) for oe in ObjEnum]
)
def test_getone_ok(id, path, mock_asset_service):

    response = client.get(f"/{path.name}/{id}")
    assert response.status_code == 200
    mock_asset_service.read.assert_called_with(
        target_type=path, webid=UUID(id)
    )
    mock_asset_service.list.assert_not_called()


@pytest.mark.parametrize("id, path", [("NOUUID", oe) for oe in ObjEnum])
def test_getone_wrong_webid(id, path, mock_asset_service):

    response = client.get(f"/{path.name}/{id}")
    assert response.status_code == 422
    mock_asset_service.read.assert_not_called()
    mock_asset_service.list.assert_not_called()


@pytest.mark.parametrize("parent, child", [("noexist", "item"), ("node", "noexist")])
def test_getall_wrong_path(parent, child, mock_asset_service):
    id = "1c8accd9-2e70-11ef-a48f-3024a9fbd4aa"
    response = client.get(f"/{parent}/{id}/{child}")
    assert response.status_code == 422
    mock_asset_service.read.assert_not_called()
    mock_asset_service.list.assert_not_called()


@pytest.mark.parametrize(
    "parent, child",
    [
        (ObjEnum.assetserver, ObjEnum.database),
        (ObjEnum.database, ObjEnum.node),
        (ObjEnum.database, ObjEnum.view),
        (ObjEnum.node, ObjEnum.item),
        (ObjEnum.item, ObjEnum.item),
    ],
)
def test_getall_ok(parent, child, mock_asset_service):

    id = "1c8accd9-2e70-11ef-a48f-3024a9fbd4aa"

    queries = ""
    response = client.get(f"/{parent.name}/{id}/{child.name}?{queries}")

    assert response.status_code == 200
    mock_asset_service.list.assert_called_with(
        parent=parent, children=child, webid=UUID(id), query_dict=ReadAllOptions(**{})
    )
    mock_asset_service.read.assert_not_called()


@pytest.mark.parametrize("id", ["NOUUID"])
def test_getall_wrongWEBID(id, mock_asset_service):

    parent_path = ObjEnum.node
    child_parent = ObjEnum.item

    response = client.get(f"/{parent_path.name}/{id}/{child_parent.name}")

    assert response.status_code == 422
    mock_asset_service.read.assert_not_called()
    mock_asset_service.list.assert_not_called()


def test_getall_ok_w_query_params(mock_asset_service):

    id = "1c8accd9-2e70-11ef-a48f-3024a9fbd4aa"
    parent_path = ObjEnum.node
    child_parent = ObjEnum.item

    queries = f"field_filter=F1111&field_filter=F2222&selected_fields=selll"

    response = client.get(f"/{parent_path.name}/{id}/{child_parent.name}?{queries}")

    # assert response.status_code == 200
    expected_query_dict = {"field_filter": ["F1111", "F2222"], "selected_fields": ["selll"]}
    print(response.json())
    mock_asset_service.list.assert_called_with(
        parent=parent_path,
        children=child_parent,
        webid=UUID(id),
        query_dict=ReadAllOptions(**expected_query_dict),
    )
    mock_asset_service.read.assert_not_called()


@pytest.mark.parametrize(
    "q",
    [
        "field_filter=F1111&field_filter=F2222&selected_fields=selll",
        "field_filter_like=FILT1&field_filter_like=FILT2&start_index=3",
        "search_full_hierarchy=True&maxCount=1000&sort_order=asc",
    ],
)
def test_getall_ok_w_query_params(q, mock_asset_service):

    id = "1c8accd9-2e70-11ef-a48f-3024a9fbd4aa"
    parent_path = ObjEnum.node
    child_parent = ObjEnum.item

    response = client.get(f"/{parent_path.name}/{id}/{child_parent.name}?{q}")

    assert response.status_code == 200
    mock_asset_service.list.assert_called_once()
    mock_asset_service.read.assert_not_called()


@pytest.mark.parametrize(
    "q",
    [
        "search_full_hierarchy=foobar",
        "start_index=foobar",
    ],
)
def test_getall_NOK_w_query_params(q, mock_asset_service):

    id = "1c8accd9-2e70-11ef-a48f-3024a9fbd4aa"
    parent_path = ObjEnum.node
    child_parent = ObjEnum.item

    response = client.get(f"/{parent_path.name}/{id}/{child_parent.name}?{q}")

    assert response.status_code == 422
    mock_asset_service.list.assert_not_called()
    mock_asset_service.read.assert_not_called()


@pytest.mark.parametrize(
    "id, body",
    [
        ("1c8accd9-2e70-11ef-a48f-3024a9fbd4aa", oe)
        for oe in [{}, {"links": [], "client_id": 'foobar'}]
    ],
)
def test_addone_ok(id, body, mock_asset_service):

    parent_path = ObjEnum.node
    child_parent = ObjEnum.item

    response = client.post(f"/{parent_path.name}/{id}/{child_parent.name}", json=body)
    assert response.status_code == 200

    mock_asset_service.read.assert_not_called()
    mock_asset_service.list.assert_not_called()
    mock_asset_service.create.assert_called_once()


@pytest.mark.parametrize("id", ["NOUUID"])
def test_addone_wrongWEBID(id, mock_asset_service):

    parent_path = ObjEnum.node
    child_parent = ObjEnum.item

    response = client.post(f"/{parent_path.name}/{id}/{child_parent.name}", json={})

    assert response.status_code == 422
    mock_asset_service.list.assert_not_called()
    mock_asset_service.read.assert_not_called()
    mock_asset_service.create.assert_not_called()
