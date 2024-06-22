""""""

import pytest

from cahier.schemas.objects import ObjEnum  # , obj_factory, is_valid_parent

###############################################################################


def obj_type(x):
    return x.__class__.__name__.lower()


@pytest.fixture
def setup_data():
    pass


def setup_function():
    # ic('setup function')
    pass


def teardown_function():
    # ic('teardown function')
    pass


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
    # o = obj_factory(ObjEnum.assetserver, SourceURL= arg)
    o = ObjEnum.assetserver.make(SourceURL=arg)
    assert obj_type(o) == "assetserver"
    assert o.base_type() == "server"
    assert str(o.source_url) == arg


def test_factories_database():
    arg = "some_db_field"
    # o = obj_factory(ObjEnum.database, DBField= arg)
    o = ObjEnum.database.make(DBField=arg)
    assert obj_type(o) == "database"
    assert o.base_type() == "root"
    assert o.db_field == arg


def test_factories_view():
    arg = "some_view_string"
    o = ObjEnum.view.make(ViewStr=arg)
    assert obj_type(o) == "view"
    assert o.base_type() == "element"
    assert o.view_str == arg


def test_factories_node():
    arg = "templated_NOD1E"
    # o = obj_factory(ObjEnum.node, Template= arg)
    o = ObjEnum.node.make(Template=arg)
    assert obj_type(o) == "node"
    assert o.base_type() == "node"
    assert o.template == arg


def test_factories_item():
    arg = "source_ITEM"
    o = ObjEnum.item.make(DataSource=arg)
    # o = obj_factory(ObjEnum.item, DataSource= arg)
    assert obj_type(o) == "item"
    assert o.base_type() == "item"
    assert o.data_source == arg


def test_factories_assetserver_hierarchy():
    assert ObjEnum.assetserver.parent_of(ObjEnum.database)
    assert ObjEnum.assetserver.parent_of(ObjEnum.view) is False
    assert ObjEnum.assetserver.parent_of(ObjEnum.node) is False
    assert ObjEnum.assetserver.parent_of(ObjEnum.item) is False
    assert ObjEnum.assetserver.parent_of(ObjEnum.assetserver) is False


def test_factories_database_hierarchy():
    assert ObjEnum.database.parent_of(ObjEnum.assetserver) is False
    assert ObjEnum.database.parent_of(ObjEnum.database) is False
    assert ObjEnum.database.parent_of(ObjEnum.view)
    assert ObjEnum.database.parent_of(ObjEnum.node)
    assert ObjEnum.database.parent_of(ObjEnum.item) is False


def test_factories_view_hierarchy():
    assert ObjEnum.view.parent_of(ObjEnum.assetserver) is False
    assert ObjEnum.view.parent_of(ObjEnum.database) is False
    assert ObjEnum.view.parent_of(ObjEnum.view) is False
    assert ObjEnum.view.parent_of(ObjEnum.node) is False
    assert ObjEnum.view.parent_of(ObjEnum.item) is False


def test_factories_node_hierarchy():
    assert ObjEnum.node.parent_of(ObjEnum.assetserver) is False
    assert ObjEnum.node.parent_of(ObjEnum.database) is False
    assert ObjEnum.node.parent_of(ObjEnum.view) is False
    assert ObjEnum.node.parent_of(ObjEnum.node)
    assert ObjEnum.node.parent_of(ObjEnum.item)


def test_factories_item_hierarchy():
    assert ObjEnum.item.parent_of(ObjEnum.assetserver) is False
    assert ObjEnum.item.parent_of(ObjEnum.database) is False
    assert ObjEnum.item.parent_of(ObjEnum.view) is False
    assert ObjEnum.item.parent_of(ObjEnum.node) is False
    assert ObjEnum.item.parent_of(ObjEnum.item)
