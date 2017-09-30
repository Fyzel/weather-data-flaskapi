"""
@author:     Fyzel@users.noreply.github.com

@copyright:  2017 Englesh.org. All rights reserved.

@license:    https://github.com/Fyzel/weather-data-flaskapi/blob/master/LICENSE

@contact:    Fyzel@users.noreply.github.com
@deffield    updated: 2017-06-14
"""

from flask_restplus import reqparse
from datetime import date, timedelta

date_range_arguments = reqparse.RequestParser()

date_range_arguments.add_argument('start-date',
                                  type=str,
                                  required=False,
                                  default=str(date.today() - timedelta(days=7)),
                                  help='Start date')

date_range_arguments.add_argument('end-date',
                                  type=str,
                                  required=False,
                                  default=str(date.today()),
                                  help='End date')
