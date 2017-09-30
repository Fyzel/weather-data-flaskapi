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
from api.weather_data_flaskapi.serializers import public_pressure
from database.models import PublicPressure

log = logging.getLogger(__name__)

ns = api.namespace('PublicPressureData',
                   description='Operations related to public pressure readings')


@ns.route('/')
class PublicPressureCollection(Resource):
    @api.marshal_list_with(public_pressure)
    @api.doc(params={'start': 'The required start date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'end': 'The required end date (e.g. 2017-01-30) for the returned records.'})
    def get(self):
        """
        Returns list of public pressure records.
        :return:
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('start', type=str, required=True)
        parser.add_argument('end', type=str, required=True)
        args = parser.parse_args()
        start = args['start']
        end = args['end']

        public_pressure_records = PublicPressure.query.filter(
            and_(PublicPressure.timestamp >= start,
                 PublicPressure.timestamp <= end)).order_by(PublicPressure.timestamp).all()

        return public_pressure_records


@ns.route('/<int:pressure_id>')
@api.response(404, 'ProtectedPressure not found.')
class PublicPressureItem(Resource):
    @api.marshal_with(public_pressure)
    def get(self, pressure_id: int):
        """
        Returns a public pressure record.
        :param pressure_id: The unique identifier of the public pressure record.
        :type pressure_id: int
        :return:
        """
        return PublicPressure.query.filter(PublicPressure.id == pressure_id).one()
