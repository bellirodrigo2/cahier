""" Routers for Cahier Builder """
from typing import Tuple
from functools import partial

from ..database import get_memory_db
from ..repositories import InMemoryRepository
# from ..database import get_sqlalchemy_db, sqlalchemy_bootstrap
# from ..repositories import SQLAlchemyRepository

from ..services import AssetService

from ..events import Event, RequestObserver

################################################################################
# SQLALCHEMY
################################################################################

# db_url = "sqlite:///./sql_app.db"
# make_session = partial(sqlalchemy_bootstrap, db_url, connect_args={"check_same_thread": False})
# make_db = partial(get_sqlalchemy_db, make_session)

# make_repo = partial(SQLAlchemyRepository, make_db)
# SQLAlchemyRepository.bootstrap()

################################################################################
# INMEMORY
################################################################################

make_repo = partial(InMemoryRepository, get_memory_db)

################################################################################
# Make Asset Service
################################################################################

make_asset_service = partial(AssetService, get_repo = make_repo)

################################################################################
# Make Event Service
################################################################################

ro = RequestObserver()
# fazer uma classe aqui com todos os metodos
# ro.observe('event1',  ro.get_http)

ro.observe('read_one', lambda ev: print(ev.data))

class ReadOneEvent(Event):
    
    def __init__(self, data: Tuple[ObjEnum, WebId]):
        Event('read_one', data)

def fire_read_one():
    return ReadOneEvent
# a funcao deve usar o mesmo tipo em data que foi colocado no event