import os

from databases import Database
from sqlalchemy import (Column, BigInteger, MetaData, String, Table,
                        create_engine, ARRAY)

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
metadata = MetaData()

movies = Table(
    'movies',
    metadata,
    Column('id', BigInteger, primary_key=True),
    Column('name', String(50)),
    Column('plot', String(250)),
    Column('genres', ARRAY(String)),
    Column('casts_id', ARRAY(BigInteger))
)

database = Database(DATABASE_URL)
