""" Routers for Cahier Builder """
from typing import Callable, Any
from functools import partial

from ..database import get_memory_db
from ..repositories import InMemoryRepository
# from ..database import get_sqlalchemy_db, sqlalchemy_bootstrap
# from ..repositories import SQLAlchemyRepository

from ..services import AssetService

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