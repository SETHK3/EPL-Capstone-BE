import routes


def register_blueprints(app):
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.users)
    app.register_blueprint(routes.teams)
    app.register_blueprint(routes.managers)
    app.register_blueprint(routes.players)
    app.register_blueprint(routes.performances)
    app.register_blueprint(routes.transfers)
