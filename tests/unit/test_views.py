from aiohttp import web

from api.views import get_vehicle, index


async def test_index_200(aiohttp_client, loop):
    """Test index view"""

    app = web.Application()
    app.router.add_get('/', index)
    client = await aiohttp_client(app)
    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'Welcome to Vehicle Builder API' in text


async def test_get_vehicle_200(aiohttp_client, loop, mocker):
    """Test get_vehicle view returns Vehicle"""

    mocked_vehicle = {'id': 1, 'name': 'vehicle1'}
    mocker.patch('api.views.get_vehicle_by_id', return_value=mocked_vehicle)
    app = web.Application()
    app.router.add_get('/ap/vehicle/{id}', get_vehicle)
    client = await aiohttp_client(app)
    resp = await client.get('/ap/vehicle/1')
    json = await resp.json()
    assert resp.status == 200
    assert json == mocked_vehicle


async def test_get_vehicle_400_wrong_id_type(aiohttp_client, loop):
    """Test get_vehicle view with wrong id type"""

    app = web.Application()
    app.router.add_get('/ap/vehicle/{id}', get_vehicle)
    client = await aiohttp_client(app)
    resp = await client.get('/ap/vehicle/wrong_id')
    assert resp.status == 400


async def test_get_vehicle_400_unexpected_error(aiohttp_client, loop, mocker):
    """Test get_vehicle view for unexpected error"""

    mocker.patch('api.views.get_vehicle_by_id', side_effect=ValueError())
    app = web.Application()
    app.router.add_get('/ap/vehicle/{id}', get_vehicle)
    client = await aiohttp_client(app)
    resp = await client.get('/ap/vehicle/1')
    assert resp.status == 400


async def test_get_vehicle_404(aiohttp_client, loop, mocker):
    """Test get_vehicle view with invalid vehicle id"""

    mocker.patch('api.views.get_vehicle_by_id', return_value=None)
    app = web.Application()
    app.router.add_get('/ap/vehicle/{id}', get_vehicle)
    client = await aiohttp_client(app)
    resp = await client.get('/ap/vehicle/1')
    assert resp.status == 404
