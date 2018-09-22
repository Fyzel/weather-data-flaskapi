"""
@author:     Fyzel@users.noreply.github.com

@copyright:  2017 Englesh.org. All rights reserved.

@license:    https://github.com/Fyzel/weather-data-flaskapi/blob/master/LICENSE

@contact:    Fyzel@users.noreply.github.com
@deffield    updated: 2017-06-14
"""

import logging
import traceback

from flask_restplus import Api
# import settings
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

api = Api(version='1.1.1',
          title='Weather Data API',
          description='A simple weather data API')


@api.errorhandler
def default_error_handler(exception):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    # if not settings.FLASK_DEBUG:
    #     return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(exception):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
