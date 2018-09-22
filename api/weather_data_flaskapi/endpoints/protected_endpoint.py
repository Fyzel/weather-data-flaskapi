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
from api.weather_data_flaskapi.business.weather_data import create_pressure, delete_pressure, update_pressure
from api.weather_data_flaskapi.business.weather_data import create_temperature, delete_temperature, update_temperature
from api.weather_data_flaskapi.serializers import humidity, pressure, temperature
from database.model_exceptions import LatitudeValueError, LongitudeValueError
from database.models import Humidity, Pressure, Temperature

log = logging.getLogger(__name__)

ns = api.namespace('protected',
                   description='Methods protected by JSON Web Token (JWT) based authentication')


@ns.route('/humidity/')
class HumidityCollection(Resource):
    @api.marshal_list_with(humidity)
    @api.doc(params={'start': 'The required start date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'end': 'The required end date (e.g. 2017-01-30) for the returned records.'})
    @jwt_required()
    def get(self):
        """
        Returns list of humidity records.
        :return:
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('start', type=str, required=True)
        parser.add_argument('end', type=str, required=True)
        parser.add_argument('city', type=str, required=True)
        parser.add_argument('province', type=str, required=True)
        parser.add_argument('country', type=str, required=True)
        args = parser.parse_args()
        start = args['start']
        end = args['end']
        city = args['city']
        province = args['province']
        country = args['country']

        records = Humidity.query.filter(
            and_(Humidity.timestamp >= start,
                 Humidity.timestamp <= end)).filter(
            and_(Humidity.city == city,
                 Humidity.province == province,
                 Humidity.country == country)).order_by(Humidity.timestamp).all()

        return records

    @api.response(201, 'Humidity successfully created.')
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


@ns.route('/humidity/<int:humidity_id>')
@api.response(404, 'Humidity not found.')
class HumidityItem(Resource):
    @api.marshal_with(humidity)
    @jwt_required()
    def get(self, humidity_id: int):
        """
        Returns a humidity record.
        :param humidity_id: The unique identifier of the humidity record.
        :type humidity_id: int
        :return:
        """
        return Humidity.query.filter(Humidity.id == humidity_id).one()

    @api.expect(humidity)
    @api.marshal_with(humidity)
    @api.response(204, 'Humidity successfully updated.')
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

    @api.response(204, 'Humidity successfully deleted.')
    @jwt_required()
    def delete(self, humidity_id: int):
        """
        Deletes a humidity record.

        :param humidity_id: The unique identifier of the humidity record.
        :type humidity_id: int
        """
        delete_humidity(humidity_id)
        return None, 204


@ns.route('/pressure/')
class PressureCollection(Resource):
    @api.marshal_list_with(pressure)
    @api.doc(params={'start': 'The required start date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'end': 'The required end date (e.g. 2017-01-30) for the returned records.'})
    @jwt_required()
    def get(self):
        """
        Returns list of pressure records.
        :return:
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('start', type=str, required=True)
        parser.add_argument('end', type=str, required=True)
        parser.add_argument('city', type=str, required=True)
        parser.add_argument('province', type=str, required=True)
        parser.add_argument('country', type=str, required=True)
        args = parser.parse_args()
        start = args['start']
        end = args['end']
        city = args['city']
        province = args['province']
        country = args['country']

        records = Pressure.query.filter(
            and_(Pressure.timestamp >= start,
                 Pressure.timestamp <= end)).filter(
            and_(Pressure.city == city,
                 Pressure.province == province,
                 Pressure.country == country)).order_by(Pressure.timestamp).all()

        return records

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


@ns.route('/pressure/<int:pressure_id>')
@api.response(404, 'Pressure not found.')
class PressureItem(Resource):
    @api.marshal_with(pressure)
    @jwt_required()
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


@ns.route('/temperature/')
class TemperatureCollection(Resource):
    @api.marshal_list_with(temperature)
    @api.doc(params={'start': 'The required start date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'end': 'The required end date (e.g. 2017-01-30) for the returned records.'})
    @jwt_required()
    def get(self):
        """
        Returns list of temperature records.
        :return:
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('start', type=str, required=True)
        parser.add_argument('end', type=str, required=True)
        parser.add_argument('city', type=str, required=True)
        parser.add_argument('province', type=str, required=True)
        parser.add_argument('country', type=str, required=True)
        args = parser.parse_args()
        start = args['start']
        end = args['end']
        city = args['city']
        province = args['province']
        country = args['country']

        records = Temperature.query.filter(
            and_(Temperature.timestamp >= start,
                 Temperature.timestamp <= end)).filter(
            and_(Temperature.city == city,
                 Temperature.province == province,
                 Temperature.country == country)).order_by(Temperature.timestamp).all()

        return records

    @api.response(201, 'Temperature successfully created.')
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


@ns.route('/temperature/<int:temperature_id>')
@api.response(404, 'Temperature not found.')
class TemperatureItem(Resource):
    @api.marshal_with(temperature)
    @jwt_required()
    def get(self, temperature_id: int):
        """
        Returns a temperature record.
        :param temperature_id: The unique identifier of the temperature record.
        :type temperature_id: int
        :return:
        """
        return Temperature.query.filter(Temperature.id == temperature_id).one()

    @api.expect(temperature)
    @api.response(204, 'Temperature successfully updated.')
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

    @api.response(204, 'Temperature successfully deleted.')
    @jwt_required()
    def delete(self, temperature_id: int):
        """
        Deletes a temperature record.

        :param temperature_id: The unique identifier of the temperature record.
        :type temperature_id: int
        """
        delete_temperature(temperature_id)
        return None, 204
