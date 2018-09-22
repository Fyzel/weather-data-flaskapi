"""
@author:     Fyzel@users.noreply.github.com

@copyright:  2017 Englesh.org. All rights reserved.

@license:    https://github.com/Fyzel/weather-data-flaskapi/blob/master/LICENSE

@contact:    Fyzel@users.noreply.github.com
@deffield    updated: 2017-06-14
"""

from os import path

import logging.config

from flask import Flask, Blueprint
from api.restplus import api
from flask_jwt import JWT, jwt_required, current_identity

from api.weather_data_flaskapi.business.security import authenticate, identity
from api.weather_data_flaskapi.endpoints.protected_endpoint import ns as protected_namespace
from api.weather_data_flaskapi.endpoints.public_endpoint import ns as public_namespace
from database import db


def create_app():
    flask_app = Flask(__name__)
    return flask_app


def initialize_app(flask_app):
    blueprint = Blueprint('weather', __name__, url_prefix='/weather')
    api.init_app(blueprint)
    api.add_namespace(protected_namespace)
    api.add_namespace(public_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)

    from database import create_database
    create_database(app=flask_app)


log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)
log = logging.getLogger(__name__)

app = create_app()
app.config.from_object('config.DevelopmentConfig')
initialize_app(app)

jwt = JWT(app, authenticate, identity)


@app.route('/')
def index():
    return 'Computer says, "Hello."'


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


def main():
    if settings.FLASK_MODE is 'DEV':
        log.info('>>>>> Starting development server at http://{host}/{context}/ <<<<<'.format(
            host=app.config['SERVER_NAME'],
            context='weather')
        )


if __name__ == "__main__":
    app.run()
