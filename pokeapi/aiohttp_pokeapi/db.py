import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, Float, String, Text, ARRAY, Date
)

meta = MetaData()

p_type = Table(
    'type', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(10), nullable=False),
    Column('description', Text, nullable=False),
    Column('total_pokemon', Integer, nullable=False),
    Column('single_pokemon', Integer, nullable=False),
    Column('double_pokemon', Integer, nullable=False),
    Column('n_moves', Integer, nullable=False),
    Column('super_effective_against', ARRAY(String(10)), nullable=False),
    Column('not_very_effective_against', ARRAY(String(10)), nullable=False),
    Column('not_effect_against', ARRAY(String(10)), nullable=False),
    Column('super_effective', ARRAY(String(10)), nullable=False),
    Column('not_very_effectivet', ARRAY(String(10)), nullable=False),
    Column('not_effect', ARRAY(String(10)), nullable=False),
    Column('avg_hp', Float, nullable=True),
    Column('avg_attack', Float, nullable=True),
    Column('avg_defense', Float, nullable=True),
    Column('avg_sp_attack', Float, nullable=True),
    Column('avg_sp_defense', Float, nullable=True),
    Column('avg_speed', Float, nullable=True),
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
