""""""
from cahier.schemas.objects import ObjEnum
from cahier.schemas.schemas import Obj, SingleOutput, ListOutput

################################################################################

def make_single_output(target_type: ObjEnum, obj: Obj)->SingleOutput:
    
    pass

def make_list_output(objs: list[Obj])->ListOutput:
    pass