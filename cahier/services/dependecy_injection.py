""" Routers for Cahier Builder """
from typing import Tuple
from functools import partial

from ..database import get_memory_db
from ..repositories import InMemoryRepository
from ..schemas import ObjEnum, WebId, Obj
# from ..database import get_sqlalchemy_db, sqlalchemy_bootstrap
# from ..repositories import SQLAlchemyRepository

from .asset import AssetService

from .events import add_event_handler, make_event

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

get_asset_service = partial(AssetService, get_repo = make_repo)

################################################################################
# Register Events
################################################################################

def pre_read_one(args: Tuple[WebId, ObjEnum | None]):
    print('Firing Pre Read', args[0], args[1])
add_event_handler(event_name='pre_read_one', callback=pre_read_one)

def post_read_one(arg: Tuple[Obj]):
    print('Firing Post Read', arg[0])
add_event_handler(event_name='post_read_one', callback=post_read_one)

get_fire_event = partial(make_event, error_handler=lambda x: print(x))
