""""""
import pytest
from unittest.mock import Mock

from icecream import ic

from cahier.schemas.objects import ObjEnum, obj_factory, is_valid_parent

################################################################################

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
    arg = 'http://example.com:8000/'
    o = obj_factory(ObjEnum.assetserver, SourceURL= arg)
    assert o.obj_type() == 'assetserver'
    assert o.base_type() == 'server'
    assert str(o.source_url) == arg


def test_factories_database():    
    arg = 'some_db_field'
    o = obj_factory(ObjEnum.database, DBField= arg)
    assert o.obj_type() == 'database'
    assert o.base_type() == 'root'
    assert o.db_field == arg


def test_factories_view():    
    arg = 'some_view_string'
    o = obj_factory(ObjEnum.view, ViewStr= arg)
    assert o.obj_type() == 'view'
    assert o.base_type() == 'element'
    assert o.view_str == arg
  
def test_factories_node():
    arg = 'templated_NOD1E'
    o = obj_factory(ObjEnum.node, Template= arg)
    assert o.obj_type() == 'node'
    assert o.base_type() == 'node'
    assert o.template == arg


def test_factories_item():    
    arg = 'source_ITEM'
    o = obj_factory(ObjEnum.item, DataSource= arg)
    assert o.obj_type() == 'item'
    assert o.base_type() == 'item'
    assert o.data_source == arg


def test_factories_assetserver_hierarchy():
    assert is_valid_parent(ObjEnum.assetserver, ObjEnum.database)
    assert is_valid_parent(ObjEnum.assetserver, ObjEnum.view) == False
    assert is_valid_parent(ObjEnum.assetserver, ObjEnum.node) == False
    assert is_valid_parent(ObjEnum.assetserver, ObjEnum.item) == False
    assert is_valid_parent(ObjEnum.assetserver, ObjEnum.assetserver) == False


def test_factories_database_hierarchy():
    assert is_valid_parent(ObjEnum.database, ObjEnum.assetserver) == False
    assert is_valid_parent(ObjEnum.database, ObjEnum.database) == False
    assert is_valid_parent(ObjEnum.database, ObjEnum.view)
    assert is_valid_parent(ObjEnum.database, ObjEnum.node)
    assert is_valid_parent(ObjEnum.database, ObjEnum.item) == False
    
    
def test_factories_view_hierarchy():
    assert is_valid_parent(ObjEnum.view, ObjEnum.assetserver) == False
    assert is_valid_parent(ObjEnum.view, ObjEnum.database) == False
    assert is_valid_parent(ObjEnum.view, ObjEnum.view) == False
    assert is_valid_parent(ObjEnum.view, ObjEnum.node) == False
    assert is_valid_parent(ObjEnum.view, ObjEnum.item) == False
    
    
def test_factories_node_hierarchy():
    assert is_valid_parent(ObjEnum.node, ObjEnum.assetserver) == False
    assert is_valid_parent(ObjEnum.node, ObjEnum.database) == False
    assert is_valid_parent(ObjEnum.node, ObjEnum.view) == False
    assert is_valid_parent(ObjEnum.node, ObjEnum.node)
    assert is_valid_parent(ObjEnum.node, ObjEnum.item)
    
def test_factories_item_hierarchy():
    assert is_valid_parent(ObjEnum.item, ObjEnum.assetserver) == False
    assert is_valid_parent(ObjEnum.item, ObjEnum.database) == False
    assert is_valid_parent(ObjEnum.item, ObjEnum.view) == False
    assert is_valid_parent(ObjEnum.item, ObjEnum.node) == False
    assert is_valid_parent(ObjEnum.item, ObjEnum.item)