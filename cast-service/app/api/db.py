import os

from databases import Database
from sqlalchemy import (Column, BigInteger, MetaData, String, Table,
                        create_engine)

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
metadata = MetaData()

casts = Table(
    'casts',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(50)),
    Column('nationality', String(20)),
)

database = Database(DATABASE_URL)
