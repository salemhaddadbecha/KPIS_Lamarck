from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

from configuration import APP_CONFIG

Base = declarative_base()

ENGINE = create_engine(APP_CONFIG.get('DB_CONN_STR'))


@contextmanager
def get_database_session():
    session = Session(bind=ENGINE, expire_on_commit=False)
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
