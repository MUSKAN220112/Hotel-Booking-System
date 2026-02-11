from flask import Flask


def create_app(config_filename=None):
    # Create the Flask application instance
    app = Flask(__name__)

    # Initialize extensions here (e.g., database, mail, etc.)
    # from .extensions import db
    # db.init_app(app)

    # Register blueprints here
    # from .blueprints.home import home_blueprint
    # app.register_blueprint(home_blueprint)

    # Set up error handlers here
    # @app.errorhandler(404)
    # def not_found(err):
    #     return {'error': 'Not Found'}, 404

    return app
