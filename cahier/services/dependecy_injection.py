""" Routers for Cahier Builder """

from functools import partial
from typing import Tuple

from cahier.database.memory_db import get_memory_db
from cahier.repositories.memory_dict import InMemoryRepository
from cahier.schemas.objects import ObjEnum
from cahier.schemas.schema import Obj, WebId
from cahier.services.asset import AssetService

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

get_asset_service = partial(AssetService, get_repo=make_repo)