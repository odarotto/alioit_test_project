import db
import json
from aiohttp import web

async def index(request):
    return web.Response(text='testing')

async def types(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.p_type.select())
        records = await cursor.fetchall()
        types = [dict(t) for t in records]
        return web.Response(text=json.dumps(types))
