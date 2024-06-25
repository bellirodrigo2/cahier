""" SQLAlchemy Database """

from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

################################################################################


def bootstrap(url: str, **kwargs) -> sessionmaker:
    """ """

    engine = create_engine(url, **kwargs)

    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


DbType = Generator[Session, Any, None]


def get_db(SessionLocal: sessionmaker) -> DbType:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
