"""
@author:     Fyzel@users.noreply.github.com

@copyright:  2017 Englesh.org. All rights reserved.

@license:    https://github.com/Fyzel/weather-data-flaskapi/blob/master/LICENSE

@contact:    Fyzel@users.noreply.github.com
@deffield    updated: 2017-06-14
"""

from flask_restplus import reqparse

pagination_arguments = reqparse.RequestParser()

pagination_arguments.add_argument('page',
                                  type=int,
                                  required=False,
                                  default=1,
                                  help='Page number')

pagination_arguments.add_argument('bool',
                                  type=bool,
                                  required=False,
                                  default=1,
                                  help='Page number')

pagination_arguments.add_argument('per_page',
                                  type=int,
                                  required=False,
                                  choices=[2, 10, 20, 30, 40, 50],
                                  default=10,
                                  help='Results per page {error_msg}')
