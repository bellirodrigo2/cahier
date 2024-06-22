""" Map Objects and hierarchies """

from enum import Enum

from cahier.schemas.base_objects import _BaseObj
from cahier.schemas.loader import load_all_plugins

###############################################################################

load_all_plugins()


def make_enum(base_class):

    deriveds = [
        [c for c in cls.__subclasses__()] for cls in base_class.__subclasses__()
    ]
    nested_classes = [item for sublist in deriveds for item in sublist]

    def name(x):
        return x.__name__.lower()

    types_map = {name(x): name(x) for x in nested_classes}
    base_map = {name(x): x.base_type() for x in nested_classes}
    parent_map = {x.base_type(): x.parent() for x in nested_classes}
    init_map = {name(x): x for x in nested_classes}

    class UtilsObjEnum:
        def parent_of(self, child):
            base_child = base_map[child.name]
            base_parent = base_map[self.name]
            possible_parents = parent_map[base_child]
            return base_parent in possible_parents

        def make(self, **kwargs):
            return init_map[self.name](**kwargs)

    ObjEnum = Enum(
        "ObjEnum",
        types_map,
        module="objects",
        qualname="objects.ObjEnum",
        type=UtilsObjEnum,
    )
    return ObjEnum


ObjEnum = make_enum(
    _BaseObj,
)

if __name__ == "__main__":
    pass
    # print('classes ', nested_classes)
    # print('parents ', parent_map)
    # print('init´s ', init_map)
    # print('bases ', base_map)
