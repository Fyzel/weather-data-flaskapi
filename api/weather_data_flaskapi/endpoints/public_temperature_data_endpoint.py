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
from api.weather_data_flaskapi.serializers import public_temperature
from database.models import PublicTemperature

log = logging.getLogger(__name__)

ns = api.namespace('PublicTemperatureData',
                   description='Operations related to public temperature readings')


@ns.route('/')
class PublicPressureCollection(Resource):
    @api.marshal_list_with(public_temperature)
    @api.doc(params={'start': 'The required start date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'end': 'The required end date (e.g. 2017-01-30) for the returned records.'})
    def get(self):
        """
        Returns list of public temperature records.
        :return:
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('start', type=str, required=True)
        parser.add_argument('end', type=str, required=True)
        args = parser.parse_args()
        start = args['start']
        end = args['end']

        public_temperature_records = PublicTemperature.query.filter(
            and_(PublicTemperature.timestamp >= start, PublicTemperature.timestamp <= end)).order_by(PublicTemperature.timestamp).all()

        return public_temperature_records


@ns.route('/<int:temperature_id>')
@api.response(404, 'ProtectedTemperature not found.')
class PublicPressureItem(Resource):
    @api.marshal_with(public_temperature)
    def get(self, temperature_id: int):
        """
        Returns a public temperature record.
        :param temperature_id: The unique identifier of the public temperature record.
        :type temperature_id: int
        :return:
        """
        return PublicTemperature.query.filter(PublicTemperature.id == temperature_id).one()
