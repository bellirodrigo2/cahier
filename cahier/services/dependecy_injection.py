""" Routers for Cahier Builder """

from functools import partial
from typing import Tuple

from cahier.database.memory_db import get_memory_db
from cahier.repositories.memory_dict import InMemoryRepository
from cahier.schemas.objects import ObjEnum
from cahier.schemas.schemas import Obj, WebId
from cahier.services.asset import AssetService
from cahier.services.events import EventHandler

###############################################################################
# SQLALCHEMY
###############################################################################

# db_url = "sqlite:///./sql_app.db"
# make_session = partial(sqlalchemy_bootstrap, db_url,
#   connect_args={"check_same_thread": False})
# make_db = partial(get_sqlalchemy_db, make_session)

# make_repo = partial(SQLAlchemyRepository, make_db)
# SQLAlchemyRepository.bootstrap()

###############################################################################
# INMEMORY
###############################################################################

make_repo = partial(InMemoryRepository, get_memory_db)

###############################################################################
# Make Asset Service
###############################################################################

get_asset_service = partial(AssetService, get_repo=make_repo, ev_handler=EventHandler)

###############################################################################
# Register Events
###############################################################################


def pre_read_one(args: Tuple[WebId, ObjEnum | None]):
    print("Firing Pre Read", args[0], args[1])


def post_read_one(arg: Tuple[Obj]):
    print("Firing Post Read", arg[0])


get_asset_service().add_event_handler("pre_read_one", pre_read_one)
