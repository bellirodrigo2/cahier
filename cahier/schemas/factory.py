""""""
from typing import Type

from . import ObjEnum, Obj, SingleOutput, ListOutput
from . import Node, Item

################################################################################


obj_map: dict[ObjEnum, Type[Obj]] = {
    ObjEnum.node: Node,
    ObjEnum.item: Item
}

def make_typed_obj(tgt_type: ObjEnum, obj: Obj)->Obj:
    pass


################################################################################


def make_single_output(obj: Obj)->SingleOutput:
    
    # CRIAR UM MAP DE TYPE PARA LINKS
    # 
    pass

def make_list_output(objs: list[Obj])->ListOutput:
    pass