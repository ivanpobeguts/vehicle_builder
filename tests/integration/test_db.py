from aiohttp import web
import aiopg.sa

from api.db import get_vehicle_by_id


async def test_get_vehicle_by_id():
    """Test getting vehicle from database"""

    engine = await aiopg.sa.create_engine(
        user='postgres',
        database='postgres',
        host='localhost',
        port=5433,
        password='postgres'
    )
    app = web.Application()
    app['db'] = engine

    result = await get_vehicle_by_id(app, 1)
    assert type(result) == dict
    assert 'id' in result

    engine.close()
    await engine.wait_closed()
