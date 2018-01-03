from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pytest

from folditdb.tables import Base

@pytest.fixture
def data():
    return dict(SID='1', PID='1', HISTORY='V1:10,V2:5,V3:4', SCORE='134.2')

@pytest.fixture(scope='module')
def session():
    DB = create_engine(environ['MYSQL_FOLDIT_TEST_DB'])
    Base.metadata.create_all(DB)
    Session = sessionmaker()
    Session.configure(bind=DB)
    s = Session()
    yield s
    s.close()
    Base.metadata.drop_all(DB)
