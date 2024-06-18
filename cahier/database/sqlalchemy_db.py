""" SQLAlchemy Database """
from typing import Generator, Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

################################################################################

def bootstrap(url: str, **kwargs)-> sessionmaker:
    """ """
        
    engine = create_engine(url, **kwargs)

    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


DbType = Generator[Session, Any, None]


def get_db(SessionLocal: sessionmaker)-> DbType:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()