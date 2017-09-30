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
from api.weather_data_flaskapi.serializers import public_humidity
from database.models import PublicHumidity

log = logging.getLogger(__name__)

ns = api.namespace('PublicHumidityData',
                   description='Operations related to public humidity readings')


@ns.route('/')
class HumidityPublicCollection(Resource):
    @api.marshal_list_with(public_humidity)
    @api.doc(params={'start': 'The required start date (e.g. 2017-01-30) for the returned records.'})
    @api.doc(params={'end': 'The required end date (e.g. 2017-01-30) for the returned records.'})
    def get(self):
        """
        Returns list of public humidity records.
        :return:
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('start', type=str, required=True)
        parser.add_argument('end', type=str, required=True)
        args = parser.parse_args()
        start = args['start']
        end = args['end']

        public_humidity_records = PublicHumidity.query.filter(
            and_(PublicHumidity.timestamp >= start, PublicHumidity.timestamp <= end)).order_by(PublicHumidity.timestamp).all()

        return public_humidity_records


@ns.route('/<int:humidity_id>')
@api.response(404, 'ProtectedHumidity not found.')
class HumidityPublicItem(Resource):
    @api.marshal_with(public_humidity)
    def get(self, humidity_id: int):
        """
        Returns a public humidity record.
        :param humidity_id: The unique identifier of the public humidity record.
        :type humidity_id: int
        :return:
        """
        return PublicHumidity.query.filter(PublicHumidity.id == humidity_id).one()
