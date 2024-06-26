""" Dependency injecion for Cahier """

from functools import partial

from cahier.repositories.database.memory_db import get_memory_db, bootstrap
from cahier.repositories.memorydao import InMemoryDAO
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

tree = bootstrap()
get_tree = partial(get_memory_db, tree=tree)

get_dao = partial(InMemoryDAO, get_tree)
container["asset_dao"] = get_dao

###############################################################################
# Make Asset Service
###############################################################################

get_asset_service = AssetService
container["asset_service"] = get_asset_service
