import logging

from flask import request
from flask_jwt import jwt_required
from flask_restplus import Resource, reqparse, abort
from sqlalchemy import and_

from api.restplus import api
from api.weather_data_api.business.weather_data import create_pressure, delete_pressure, update_pressure
from api.weather_data_api.serializers import pressure
from database.model_exceptions import LatitudeValueError, LongitudeValueError
from database.models import Pressure

log = logging.getLogger(__name__)

ns = api.namespace('pressures',
                   description='Operations related to pressure readings')


@ns.route('/')
class PressureCollection(Resource):
    @api.marshal_list_with(pressure)
    @api.doc(params={'start': 'The required start date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'end': 'The required end date (e.g. 2017-01-30) for the returned records.'})
    def get(self):
        """
        Returns list of pressure records.
        :return:
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('start', type=str, required=True)
        parser.add_argument('end', type=str, required=True)
        args = parser.parse_args()
        start = args['start']
        end = args['end']

        pressures = Pressure.query.filter(
            and_(Pressure.timestamp >= start, Pressure.timestamp <= end)).order_by(Pressure.timestamp).all()

        return pressures

    @api.response(201, 'Pressure successfully created.')
    @api.expect(pressure)
    @api.marshal_with(pressure)
    @jwt_required()
    def post(self):
        """
        Creates a new pressure record.
        :return:
        """
        data = request.json

        try:
            data = create_pressure(data)
        except LatitudeValueError:
            abort(400, 'Bad request: latitude out of range (-90 to 90)')
        except LongitudeValueError:
            abort(400, 'Bad request: longitude out of range (-180 to 180)')

        return data, 201


@ns.route('/<int:pressure_id>')
@api.response(404, 'Pressure not found.')
class PressureItem(Resource):
    @api.marshal_with(pressure)
    def get(self, pressure_id: int):
        """
        Returns a pressure record.
        :param pressure_id: The unique identifier of the pressure record.
        :type pressure_id: int
        :return:
        """
        return Pressure.query.filter(Pressure.id == pressure_id).one()

    @api.expect(pressure)
    @api.response(204, 'Pressure successfully updated.')
    @api.marshal_with(pressure)
    @jwt_required()
    def put(self, pressure_id: int):
        """
        Updates a pressure record.

        Use this method to change the values for a pressure record.

        * Send a JSON object with the new data in the request body.

        ```
        {
            "value": 14.4924,
            "value_units": "Pa",
            "value_error_range": 0.192573,
            "timestamp": "0525-05-07T21:46:04",
            "elevation": "66166.1257",
            "elevation_units": "m",
            "latitude": 54.788803,
            "longitude": -5.176766
        }
        ```

        * Specify the ID of the pressure to modify in the request URL path.
        :param pressure_id: The unique identifier of the pressure record.
        :type pressure_id: int
        """
        data = request.json

        try:
            data = update_pressure(pressure_id, data)
        except LatitudeValueError:
            abort(400, 'Bad request: latitude out of range (-90 to 90)')
        except LongitudeValueError:
            abort(400, 'Bad request: longitude out of range (-180 to 180)')

        return data, 204

    @api.response(204, 'Pressure successfully deleted.')
    @jwt_required()
    def delete(self, pressure_id: int):
        """
        Deletes a pressure record.

        :param pressure_id: The unique identifier of the pressure record.
        :type pressure_id: int
        """
        delete_pressure(pressure_id)
        return None, 204
