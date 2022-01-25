import os
from flask import Flask, jsonify
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# init the app
db = SQLAlchemy()

def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)

    from src.api.ping import ping_blueprint
    app.register_blueprint(ping_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app' : app, 'db' : db}

    return app

