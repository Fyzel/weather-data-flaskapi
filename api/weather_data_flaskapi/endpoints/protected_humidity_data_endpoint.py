"""
@author:     Fyzel@users.noreply.github.com

@copyright:  2017 Englesh.org. All rights reserved.

@license:    https://github.com/Fyzel/weather-data-flaskapi/blob/master/LICENSE

@contact:    Fyzel@users.noreply.github.com
@deffield    updated: 2017-06-14
"""

import logging

from flask import request
from flask_jwt import jwt_required
from flask_restplus import Resource, reqparse, abort
from sqlalchemy import and_

from api.restplus import api
from api.weather_data_flaskapi.business.weather_data import create_humidity, delete_humidity, update_humidity
from api.weather_data_flaskapi.serializers import humidity
from database.model_exceptions import LatitudeValueError, LongitudeValueError
from database.models import ProtectedHumidity

log = logging.getLogger(__name__)

ns = api.namespace('ProtectedHumidityData',
                   description='Operations related to humidity readings')


@ns.route('/')
class ProtectedHumidityCollection(Resource):
    @api.marshal_list_with(humidity)
    @api.doc(params={'start': 'The required start date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'end': 'The required end date (e.g. 2017-01-30) for the returned records.'})
    @jwt_required()
    def get(self):
        """
        Returns list of protected humidity records.
        :return:
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('start', type=str, required=True)
        parser.add_argument('end', type=str, required=True)
        args = parser.parse_args()
        start = args['start']
        end = args['end']

        protected_records = ProtectedHumidity.query.filter(
            and_(ProtectedHumidity.timestamp >= start, ProtectedHumidity.timestamp <= end)).order_by(ProtectedHumidity.timestamp).all()

        return protected_records

    @api.response(201, 'ProtectedHumidity successfully created.')
    @api.expect(humidity)
    @api.marshal_with(humidity)
    @jwt_required()
    def post(self):
        """
        Creates a new humidity record.
        :return:
        """
        data = request.json

        try:
            data = create_humidity(data)
        except LatitudeValueError:
            abort(400, 'Bad request: latitude out of range (-90 to 90)')
        except LongitudeValueError:
            abort(400, 'Bad request: longitude out of range (-180 to 180)')

        return data, 201


@ns.route('/<int:humidity_id>')
@api.response(404, 'ProtectedHumidity not found.')
class ProtectedHumidityItem(Resource):
    @api.marshal_with(humidity)
    @jwt_required()
    def get(self, humidity_id: int):
        """
        Returns a protected humidity record.
        :param humidity_id: The unique identifier of the humidity record.
        :type humidity_id: int
        :return:
        """
        return ProtectedHumidity.query.filter(ProtectedHumidity.id == humidity_id).one()

    @api.expect(humidity)
    @api.response(204, 'ProtectedHumidity successfully updated.')
    @api.marshal_with(humidity)
    @jwt_required()
    def put(self, humidity_id: int):
        """
        Updates a humidity record.

        Use this method to change the values for a humidity record.

        * Send a JSON object with the new data in the request body.

        ```
        {
            "value": 14.4924,
            "value_units": "RH",
            "value_error_range": 0.192573,
            "latitude": 54.788803,
            "latitude_public": 54.788,
            "longitude": -5.176766,
            "longitude_public": -5.176,
            "city": "Toronto",
            "province": "ON",
            "country": "CA",
            "elevation": 66166.1257,
            "elevation_units": "m",
            "timestamp": "0525-05-07T21:46:04"
        }
        ```

        * Specify the ID of the humidity to modify in the request URL path.
        :param humidity_id: The unique identifier of the humidity record.
        :type humidity_id: int
        """
        data = request.json

        try:
            data = update_humidity(humidity_id, data)
        except LatitudeValueError:
            abort(400, 'Bad request: latitude out of range (-90 to 90)')
        except LongitudeValueError:
            abort(400, 'Bad request: longitude out of range (-180 to 180)')
        return data, 204

    @api.response(204, 'ProtectedHumidity successfully deleted.')
    @jwt_required()
    def delete(self, humidity_id: int):
        """
        Deletes a humidity record.

        :param humidity_id: The unique identifier of the humidity record.
        :type humidity_id: int
        """
        delete_humidity(humidity_id)
        return None, 204
