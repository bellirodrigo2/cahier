""" Map Objects and hierarchies """
from typing import Annotated
from enum import Enum
import os
import importlib

from pydantic import Field

from cahier.schemas.base_objects import _BaseObj, _NodeObj, _ItemObj, _ElementObj

################################################################################

def get_plugins(path: str)->list[str]:
    """Get the python files from parent 'plugin' folder."""
    
    walk_list:list[str] = list(next(os.walk(f'{path}/plugins'), (None, None, []))[2])
    return [f'plugins.{x}'.replace('.py','') 
            for x in walk_list 
                if x.endswith('.py') and x.startswith('__init__') == False]

def import_module(name: str):
    """Imports a module given a name."""

    return importlib.import_module(f'cahier.schemas.{name}')

def load_all_plugins(plugins: list[str]) -> None:
    """Loads the plugins defined in the plugins list."""
    
    for plugin_file in plugins:
        plugin = import_module(plugin_file)

# Load Plugins Here
plugins = get_plugins(os.path.dirname(__file__))
load_all_plugins(plugins)


deriveds = [[c for c in cls.__subclasses__()] for cls in _BaseObj.__subclasses__()]
nested_classes = [item for sublist in deriveds for item in sublist]

parent_map = {x.base_type(): x.parent() for x in nested_classes}
types_map = {x.obj_type(): x.obj_type() for x in nested_classes}
base_map = {x.obj_type(): x.base_type() for x in nested_classes}
init_map = {x.obj_type(): x for x in nested_classes}

ObjEnum = Enum(
    'ObjEnum',
    types_map,
    module='objects',
    qualname='objects.ObjEnum',
    )

def obj_factory(obj_type: ObjEnum, **kwargs):
    return init_map[obj_type.name](**kwargs)

def is_valid_parent(parent: ObjEnum, child: ObjEnum):
    base_child = base_map[child.name]
    base_parent = base_map[parent.name]
    possible_parents = parent_map[base_child]
    return base_parent in possible_parents

if __name__ == '__main__':
    
    print('classes ', nested_classes)
    print('parents ', parent_map)
    print('init´s ', init_map)
    print('bases ', base_map)