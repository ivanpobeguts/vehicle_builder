import logging

from aiohttp import web
from aiohttp_swagger import setup_swagger
from aiomisc.log import basic_config
from argparse import ArgumentParser, Namespace

from api.db import init_db, close_db
from api.config import add_config
from api.routes import setup_routes

LOGGER = logging.getLogger(__name__)


async def app_factory(args: Namespace) -> web.Application:
    """Inits application with settings, documentation and routing"""

    basic_config(level=args.log_level)

    app = web.Application()
    add_config(app)
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    setup_routes(app)
    setup_swagger(
        app,
        swagger_url='/api/v1/doc',
        description='Vehicle Builder API documentation',
        title='Vehicle Builder API',
        api_version='1.0.0'
    )
    LOGGER.info('Application configured')
    return app


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--api-host', default='0.0.0.0',
                        help='IPv4/IPv6 address API server would listen on')
    parser.add_argument('--api-port', type=int, default=8080,
                        help='TCP port API server would listen on')
    parser.add_argument('--log_level', type=str, default='debug',
                        help='Logging level')
    args = parser.parse_args()

    web.run_app(app_factory(args), host=args.api_host, port=args.api_port)
