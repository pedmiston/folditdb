#!/usr/bin/env python
from os import environ
from sqlalchemy import create_engine
from folditdb.tables import Base
DB = create_engine(environ['MYSQL_FOLDIT_TEST_DB'])
Base.metadata.drop_all(DB)
