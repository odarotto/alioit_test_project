from views import index, types

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/types', types)
