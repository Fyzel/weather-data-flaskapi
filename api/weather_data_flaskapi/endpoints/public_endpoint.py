"""
@author:     Fyzel@users.noreply.github.com

@copyright:  2017 Englesh.org. All rights reserved.

@license:    https://github.com/Fyzel/weather-data-flaskapi/blob/master/LICENSE

@contact:    Fyzel@users.noreply.github.com
@deffield    updated: 2017-06-14
"""

import logging

from flask_restplus import Resource, reqparse
from sqlalchemy import and_

from api.restplus import api
from api.weather_data_flaskapi.serializers import public_humidity, public_pressure, public_temperature
from database.models import Humidity, Pressure, Temperature

log = logging.getLogger(__name__)

ns = api.namespace('public',
                   description='Public methods')


@ns.route('/humidity/')
class PublicHumidityCollection(Resource):
    @api.marshal_list_with(public_humidity)
    @api.doc(params={'start': 'The required start date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'end': 'The required end date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'city': 'The required city for the returned records.'})
    def get(self):
        """
        Returns list of public humidity records.
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


@ns.route('/humidity/<int:humidity_id>')
@api.response(404, 'PublicHumidity not found.')
class PublicHumidityItem(Resource):
    @api.marshal_with(public_humidity)
    def get(self, humidity_id: int):
        """
        Returns a public humidity record.
        :param humidity_id: The unique identifier of the public humidity record.
        :type humidity_id: int
        :return:
        """
        return Humidity.query.filter(Humidity.id == humidity_id).one()


@ns.route('/pressure/')
class PublicPressureCollection(Resource):
    @api.marshal_list_with(public_pressure)
    @api.doc(params={'start': 'The required start date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'end': 'The required end date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'city': 'The required city for the returned records.'})
    def get(self):
        """
        Returns list of public pressure records.
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


@ns.route('/pressure/<int:pressure_id>')
@api.response(404, 'PublicPressure not found.')
class PublicPressureItem(Resource):
    @api.marshal_with(public_pressure)
    def get(self, pressure_id: int):
        """
        Returns a public pressure record.
        :param pressure_id: The unique identifier of the public pressure record.
        :type pressure_id: int
        :return:
        """
        return Pressure.query.filter(Pressure.id == pressure_id).one()


@ns.route('/temperature/')
class PublicTemperatureCollection(Resource):
    @api.marshal_list_with(public_temperature)
    @api.doc(params={'start': 'The required start date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'end': 'The required end date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'city': 'The required city for the returned records.'})
    def get(self):
        """
        Returns list of public temperature records.
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


@ns.route('/temperature/<int:temperature_id>')
@api.response(404, 'PublicTemperature not found.')
class PublicTemperatureItem(Resource):
    @api.marshal_with(public_temperature)
    def get(self, temperature_id: int):
        """
        Returns a public temperature record.
        :param temperature_id: The unique identifier of the public temperature record.
        :type temperature_id: int
        :return:
        """
        return Temperature.query.filter(Temperature.id == temperature_id).one()
