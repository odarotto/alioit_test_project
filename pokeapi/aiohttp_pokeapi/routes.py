from views import index, pokemon

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/pokemon', pokemon)
