import logging

from aiohttp import web
from aiohttp_swagger import swagger_path

from .db import get_vehicle_by_id

LOGGER = logging.getLogger(__name__)


@swagger_path("docs/index.yaml")
async def index(request):
    """Get index welcome page"""
    return web.json_response('Welcome to Vehicle Builder API')


@swagger_path("docs/vehicle.yaml")
async def get_vehicle(request):
    """Get vehicle by id"""

    try:
        vehicle_id = int(request.match_info.get('id'))
        vehicle_rows = await get_vehicle_by_id(request.app, vehicle_id)
    except ValueError:
        LOGGER.info('Type error: Vehicle id type must be int')
        return web.json_response(status=400, text='Vehicle id type must be int')
    except Exception:
        LOGGER.info('Unexpected error')
        return web.json_response(status=400, text='Internal error')

    if not vehicle_rows:
        LOGGER.info(f'Vehicle with id {vehicle_id} not found')
        raise web.HTTPNotFound()
    return web.json_response(data=vehicle_rows)
