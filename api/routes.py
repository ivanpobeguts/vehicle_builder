from .views import index, get_vehicle


def setup_routes(app):
    """Adds routing config for API"""

    app.router.add_get('/', index)
    app.router.add_get('/api/vehicle/{id}', get_vehicle)
