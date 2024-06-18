""" SQLAlchemy Repository """
from typing import Callable

from sqlalchemy.orm import DeclarativeBase

from ..database.sqlalchemy_db import DbType
from ..schemas import WebId, Obj


################################################################################

class _Base(DeclarativeBase):
    pass

class SQLAlchemyRepository:
    
    def __init__(self, get_db: Callable[[], DbType]) -> None:
        self.get_db = get_db
    
    @staticmethod
    def bootstrap(cls)->None:
        _Base.metadata.create_all()
    
    def get_one(self, web_id: WebId)->Obj:
        pass
        # db = self.get_db()
        # one_obj = db.query(XXX).filter(XXX.WebId == web_id).first()
    
    def get_all(self, web_id: WebId)->list[Obj]:
        pass
        # db = self.get_db()
        # all_obj = db.query(XXX).all()
    
    def add_one(self, parent_webid: WebId, obj: Obj)->None:
        pass
        # db = self.get_db()
        # db_item = XXX(**obj.dict(), other_param=???)
        # db.add(db_item)
        # db.commit()
        # db.refresh(db_item)
        # return db_item