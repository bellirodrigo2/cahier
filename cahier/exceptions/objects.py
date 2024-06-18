""" Objects Related Exceptions """
from functools import partial

from ..schemas import ObjEnum
from ..exchandlers import CahierException, create_exception_handler 

################################################################################


class ObjError(CahierException):
    """ Exceptions Related to the Objects Service """
    pass

class TypeHierarchyError(ObjError):
    """ failure in the type hierarchy. parent and children types are incompatible """
    
    def __init__(self, parent_type: ObjEnum, children_type: ObjEnum):
        ObjError.__init__(self, f'Type Hierarchy Error. \
            Object of type {parent_type=} can´t have a children of type {children_type=}')


class InconsistentTypeError(ObjError):
    """ failure in the 'expected' vs 'actual' type """
    
    def __init__(self, expected: ObjEnum, actual: ObjEnum):
        ObjError.__init__(self, f'Type Expectation Error. \
            Expected a type {expected=}, but got a(n) {actual=}')

type_hierarchy_handler = create_exception_handler(status_code=400, initial_detail='ERROR')
inconsistent_type_handler = create_exception_handler(status_code=400, initial_detail='ERROR')