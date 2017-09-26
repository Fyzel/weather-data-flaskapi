import logging

from flask import request
from flask_jwt import jwt_required
from flask_restplus import Resource, reqparse, abort
from sqlalchemy import and_

from api.restplus import api
from api.weather_data_api.business.weather_data import create_temperature, delete_temperature, update_temperature
from api.weather_data_api.serializers import temperature
from database.model_exceptions import LatitudeValueError, LongitudeValueError
from database.models import ProtectedTemperature

log = logging.getLogger(__name__)

ns = api.namespace('ProtectedTemperatureData',
                   description='Operations related to temperature readings')


@ns.route('/')
class ProtectedTemperatureCollection(Resource):
    @api.marshal_list_with(temperature)
    @api.doc(params={'start': 'The required start date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'end': 'The required end date (e.g. 2017-01-30) for the returned records.'})
    @jwt_required()
    def get(self):
        """
        Returns list of protected temperature records.
        :return:
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('start', type=str, required=True)
        parser.add_argument('end', type=str, required=True)
        args = parser.parse_args()
        start = args['start']
        end = args['end']

        protected_records = ProtectedTemperature.query.filter(
            and_(ProtectedTemperature.timestamp >= start, ProtectedTemperature.timestamp <= end)).order_by(ProtectedTemperature.timestamp).all()

        return protected_records

    @api.response(201, 'ProtectedTemperature successfully created.')
    @api.expect(temperature)
    @api.marshal_with(temperature)
    @jwt_required()
    def post(self):
        """
        Creates a new temperature record.
        :return:
        """
        data = request.json
        try:
            data = create_temperature(data)
        except LatitudeValueError:
            abort(400, 'Bad request: latitude out of range (-90 to 90)')
        except LongitudeValueError:
            abort(400, 'Bad request: longitude out of range (-180 to 180)')

        return data, 201


@ns.route('/<int:temperature_id>')
@api.response(404, 'ProtectedTemperature not found.')
class ProtectedTemperatureItem(Resource):
    @api.marshal_with(temperature)
    @jwt_required()
    def get(self, temperature_id: int):
        """
        Returns a protected temperature record.
        :param temperature_id: The unique identifier of the temperature record.
        :type temperature_id: int
        :return:
        """
        return ProtectedTemperature.query.filter(ProtectedTemperature.id == temperature_id).one()

    @api.expect(temperature)
    @api.response(204, 'ProtectedTemperature successfully updated.')
    @api.marshal_with(temperature)
    @jwt_required()
    def put(self, temperature_id: int):
        """
        Updates a temperature record.

        Use this method to change the values for a temperature.

        * Send a JSON object with the new data in the request body.

        ```
        {
            "value": 14.4924,
            "value_units": "C",
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

        * Specify the ID of the temperature to modify in the request URL path.
        :param temperature_id: The unique identifier of the temperature record.
        :type temperature_id: int
        """
        data = request.json

        try:
            data = update_temperature(temperature_id, data)
        except LatitudeValueError:
            abort(400, 'Bad request: latitude out of range (-90 to 90)')
        except LongitudeValueError:
            abort(400, 'Bad request: longitude out of range (-180 to 180)')

        return data, 204

    @api.response(204, 'ProtectedTemperature successfully deleted.')
    @jwt_required()
    def delete(self, temperature_id: int):
        """
        Deletes a temperature record.

        :param temperature_id: The unique identifier of the temperature record.
        :type temperature_id: int
        """
        delete_temperature(temperature_id)
        return None, 204
