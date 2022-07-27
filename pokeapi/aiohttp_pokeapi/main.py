from aiohttp import web
from settings import config
from routes import setup_routes
from db import pg_context, pokemon
from init_db import init_db_main, get_engine
from extraction import main
from sqlalchemy import insert, MetaData
import selectors  # isort:skip # noqa: F401
import asyncio

selectors._PollLikeSelector.modify = (  # type: ignore
    selectors._BaseSelectorImpl.modify  # type: ignore
)  # noqa: E402

if __name__ == '__main__':
    # Setup database
    # ----------------------------------------------------------------------------------------------
    init_db_main()
    # ----------------------------------------------------------------------------------------------
    # Start data extraction
    # ----------------------------------------------------------------------------------------------
    data = asyncio.get_event_loop().run_until_complete(main())
    # ----------------------------------------------------------------------------------------------
    # Insert data into database
    # ----------------------------------------------------------------------------------------------
    # table = MetaData.tables['pokemon']
    engine = get_engine()
    with engine.connect() as conn:
        for entry in data:
            query = insert(pokemon).values(
                name=entry['name'], _id=entry['id'], _type = entry['type'],
                species=entry['species'], height=entry['height'], weight=entry['weight']
            )
            compiled = query.compile()
            result = conn.execute(query)
        # conn.commit()
    # ----------------------------------------------------------------------------------------------
    # Setup app
    # ----------------------------------------------------------------------------------------------
    print(f'[!] API Started!')
    app = web.Application()
    app['config'] = config
    setup_routes(app)
    app.cleanup_ctx.append(pg_context)
    web.run_app(app)
