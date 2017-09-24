from flask_restplus import reqparse
from datetime import date, timedelta

date_range_pagination_arguments = reqparse.RequestParser()

date_range_pagination_arguments.add_argument('start-date',
                                             type=str,
                                             required=False,
                                             default=str(date.today() - timedelta(days=7)),
                                             help='Start date')

date_range_pagination_arguments.add_argument('end-date',
                                             type=str,
                                             required=False,
                                             default=str(date.today()),
                                             help='End date')

date_range_pagination_arguments.add_argument('page',
                                             type=int,
                                             required=False,
                                             default=1,
                                             help='Page number')

date_range_pagination_arguments.add_argument('bool',
                                             type=bool,
                                             required=False,
                                             default=1,
                                             help='Page number')

date_range_pagination_arguments.add_argument('per_page',
                                             type=int,
                                             required=False,
                                             choices=[2, 10, 20, 30, 40, 50],
                                             default=10,
                                             help='Results per page {error_msg}')
