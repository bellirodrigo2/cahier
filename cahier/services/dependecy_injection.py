""" Dependency injecion for Cahier """

from functools import partial

from cahier.database.memory_db import get_memory_db
from cahier.repositories.memory_repo import InMemoryRepository
from cahier.services.asset import AssetService

###############################################################################
# SQLALCHEMY
###############################################################################

container = {}

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
container["make_repo"] = make_repo
###############################################################################
# Make Asset Service
###############################################################################

make_asset = partial(AssetService, get_repo=make_repo)
container["make_asset"] = make_asset
