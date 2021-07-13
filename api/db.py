from typing import Dict, Optional

from aiohttp.web_app import Application
import aiopg.sa


def get_vehicle_query(vehicle_id: int) -> str:
    """Creates Postgresql query to fetch Vehicle nested structure"""

    feature_func_query = '''
        SELECT v_feature.id,
        v_feature.name,
        json_agg(json_build_object('id', v_func.id, 'name', v_func.name)) as functions
        FROM vehicle_feature as v_feature
        LEFT JOIN vehicle_function as v_func ON v_func.id = ANY(v_feature.function_list)
        GROUP BY v_feature.id, v_feature.name
        '''
    subgroup_feature_query = f'''
        SELECT vsg.id,
        vsg.name,
        vsg.is_set,
        json_agg(json_build_object('id', feature.id, 'name', feature.name, 'functions', feature.functions)) as features
        FROM vehicle_subgroup as vsg
        LEFT JOIN ({feature_func_query}) as feature ON feature.id = ANY(vsg.feature_list)
        GROUP BY vsg.id, vsg.name, vsg.is_set
        '''
    group_subgroup_query = f'''
        SELECT vg.id,
        vg.name,
        COALESCE(json_agg(json_build_object(
        'id', feature.id, 'name', feature.name, 'functions', feature.functions))
        FILTER (WHERE feature.id IS NOT NULL), '[]') as features,
        COALESCE(json_agg(json_build_object(
        'id', vsg.id, 'name', vsg.name, 'is_set', vsg.is_set, 'features', vsg.features))
        FILTER (WHERE vsg.id IS NOT NULL), '[]') as subgroups
        FROM vehicle_group as vg
        LEFT JOIN ({subgroup_feature_query}) as vsg ON vsg.id = ANY(vg.subgroup_list)
        LEFT JOIN ({feature_func_query}) as feature ON feature.id = ANY(vg.feature_list)
        GROUP BY vg.id, vg.name
        '''
    query = f'''
        SELECT v.id,
        v.name,
        json_agg(json_build_object('id', g.id, 'name', g.name, 'subgroups', g.subgroups, 'features', g.features))
        as groups
        FROM vehicle as v
        LEFT JOIN ({group_subgroup_query}) as g ON g.id = ANY(v.group_list)
        WHERE v.id = {vehicle_id}
        GROUP BY v.id, v.name
        '''
    return query


async def get_vehicle_by_id(app: Application, vehicle_id: int) -> Optional[Dict]:
    """Gets vehicle by id (int) from database"""

    async with app['db'].acquire() as conn:
        cursor = await conn.execute(get_vehicle_query(vehicle_id))
        records = await cursor.fetchone()
        return dict(records) if records else None


async def init_db(app: Application):
    """Initializes application with Postgre database config to make queries"""

    engine = await aiopg.sa.create_engine(
        user=app['pg_user'],
        database=app['pg_db'],
        host=app['pg_host'],
        port=app['pg_port'],
        password=app['pg_password']
    )
    app['db'] = engine


async def close_db(app: Application):
    """Closes database connection when the application is down"""

    app['db'].close()
    await app['db'].wait_closed()
