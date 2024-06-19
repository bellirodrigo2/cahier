""" Routers for Cahier Builder """
from typing import Tuple
from functools import partial

from ..database import get_memory_db
from ..repositories import InMemoryRepository
from ..schemas import ObjEnum, WebId
# from ..database import get_sqlalchemy_db, sqlalchemy_bootstrap
# from ..repositories import SQLAlchemyRepository

from .asset import AssetService, PreReadOneEvent, PostReadOneEvent
from .events import Observer
from ..interfaces import EventInterface

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
# Register Events
################################################################################

def pre_read(ev: Tuple[ObjEnum, WebId]):
    print('Firing', ev[0], ev[1])

# como fazer para o callback ter o mesmo tipo de "data" dor event ????

Observer.observe(event_name=PreReadOneEvent, callback=pre_read)