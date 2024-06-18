""" In Memory Repository """
from typing import Callable

from ..database.memory_db import ObjMemoryInterface
from ..database.memory_db import make_obj

from ..schemas import WebId, Obj

################################################################################

# Fake objects actually have working implementations, but usually take some shortcut which makes them not suitable for production (an InMemoryTestDatabase is a good example).

class InMemoryRepository:
    
    def __init__(self, get_db: Callable[[], dict[WebId, ObjMemoryInterface]]) -> None:
        self.get_db = get_db
    
    @staticmethod
    def bootstrap(cls)->None:
        pass
    
    def get_one(self, web_id: WebId)->Obj:
        db = self.get_db()
        return db[web_id].obj
    
    def get_all(self, web_id: WebId)->list[Obj]:
        db = self.get_db()
        return [om.obj for om in db.values() if om.parent == web_id]
    
    def add_one(self, parent_webid: WebId, obj: Obj)->None:
        db = self.get_db()
        db[obj.web_id] = make_obj(obj, parent_webid)