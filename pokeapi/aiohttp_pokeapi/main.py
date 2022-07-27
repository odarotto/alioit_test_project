from aiohttp import web
from settings import config
from routes import setup_routes
from db import pg_context
from init_db import init_db_main
import selectors  # isort:skip # noqa: F401

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
    # ----------------------------------------------------------------------------------------------
    # Setup app
    # ----------------------------------------------------------------------------------------------
    app = web.Application()
    app['config'] = config
    setup_routes(app)
    app.cleanup_ctx.append(pg_context)

    web.run_app(app)
