import os

from aiohttp.web import Application
import yaml


def add_config(app: Application):
    path = os.environ.get('VEHICLE_BUILDER_CFG_PATH', 'config/prod.yaml')
    with open(path) as f:
        config = yaml.safe_load(f)
    app['pg_db'] = config['postgres']['database']
    app['pg_user'] = config['postgres']['user']
    app['pg_password'] = config['postgres']['password']
    app['pg_host'] = config['postgres']['host']
    app['pg_port'] = config['postgres']['port']
