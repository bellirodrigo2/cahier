""" Dependency injecion for Cahier """

from functools import partial

from cahier.repositories.database.memory_db import get_memory_db
from cahier.repositories.memory_repo import InMemoryRepository
from cahier.services.asset import AssetService

container = {}

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

get_dao = partial(InMemoryRepository, get_memory_db)
container["asset_dao"] = get_dao
###############################################################################
# Make Asset Service
###############################################################################

get_asset_service = partial(AssetService, get_dao=get_dao)
container["asset_service"] = get_asset_service
