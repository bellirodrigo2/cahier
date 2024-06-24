""""""

import pytest

from cahier.schemas.schemas import ObjEnum, is_valid_parent

###############################################################################

def obj_type(x):
    return x.__class__.__name__.lower()

def test_enums():
    ObjEnum.assetserver
    ObjEnum.database
    ObjEnum.view
    ObjEnum.node
    ObjEnum.item
    with pytest.raises(Exception):
        ObjEnum.ndie


def test_factories_assetserver():
    arg = "http://example.com:8000/"
    o = ObjEnum.assetserver
    m = o.make(source_url=arg)
    assert o.value == "assetserver"
    assert o.base_type == "server"
    assert str(m.source_url) == arg


def test_factories_database():
    arg = "some_db_field"
    o = ObjEnum.database
    m = o.make(host=arg)
    assert o.value == "database"
    assert o.base_type == "root"
    assert m.host == arg


def test_factories_view():
    arg = "some_view_string"
    o = ObjEnum.view
    m = o.make(view_str=arg)
    assert o.value == "view"
    assert o.base_type == "element"
    assert m.view_str == arg


def test_factories_node():
    arg = "templated_NOD1E"
    o = ObjEnum.node
    m = o.make(template=arg)
    assert o.value == "node"
    assert o.base_type == "node"
    assert m.template == arg


def test_factories_item():
    arg = int
    o = ObjEnum.item
    m = o.make(type=arg)
    assert o.value == "item"
    assert o.base_type == "item"
    assert m.type == arg


# def test_factories_assetserver_hierarchy():
#     assert ObjEnum.assetserver.parent_of(ObjEnum.database)
#     assert ObjEnum.assetserver.parent_of(ObjEnum.view) is False
#     assert ObjEnum.assetserver.parent_of(ObjEnum.node) is False
#     assert ObjEnum.assetserver.parent_of(ObjEnum.item) is False
#     assert ObjEnum.assetserver.parent_of(ObjEnum.assetserver) is False


# def test_factories_database_hierarchy():
#     assert ObjEnum.database.parent_of(ObjEnum.assetserver) is False
#     assert ObjEnum.database.parent_of(ObjEnum.database) is False
#     assert ObjEnum.database.parent_of(ObjEnum.view)
#     assert ObjEnum.database.parent_of(ObjEnum.node)
#     assert ObjEnum.database.parent_of(ObjEnum.item) is False


# def test_factories_view_hierarchy():
#     assert ObjEnum.view.parent_of(ObjEnum.assetserver) is False
#     assert ObjEnum.view.parent_of(ObjEnum.database) is False
#     assert ObjEnum.view.parent_of(ObjEnum.view) is False
#     assert ObjEnum.view.parent_of(ObjEnum.node) is False
#     assert ObjEnum.view.parent_of(ObjEnum.item) is False


# def test_factories_node_hierarchy():
#     assert ObjEnum.node.parent_of(ObjEnum.assetserver) is False
#     assert ObjEnum.node.parent_of(ObjEnum.database) is False
#     assert ObjEnum.node.parent_of(ObjEnum.view) is False
#     assert ObjEnum.node.parent_of(ObjEnum.node)
#     assert ObjEnum.node.parent_of(ObjEnum.item)


# def test_factories_item_hierarchy():
#     assert ObjEnum.item.parent_of(ObjEnum.assetserver) is False
#     assert ObjEnum.item.parent_of(ObjEnum.database) is False
#     assert ObjEnum.item.parent_of(ObjEnum.view) is False
#     assert ObjEnum.item.parent_of(ObjEnum.node) is False
#     assert ObjEnum.item.parent_of(ObjEnum.item)
