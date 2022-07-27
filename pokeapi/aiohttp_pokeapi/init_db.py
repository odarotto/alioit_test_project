from sqlalchemy import create_engine, MetaData
from settings import config
from db import p_type

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[p_type])

def init_db_main():
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)
    create_tables(engine)
    print(f'[!] Databases created.')

