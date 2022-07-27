import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, ARRAY
)

__all__ = ['pokemon']

meta = MetaData()

pokemon = Table(
    'pokemon', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(30), nullable=False),
    Column('_id', Integer),
    Column('_type', ARRAY(String(30)), nullable=False),
    Column('species', String(100), nullable=False),
    Column('height', String(100), nullable=False),
    Column('weight', String(100), nullable=False),
)

async def pg_context(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize']
    )
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()
