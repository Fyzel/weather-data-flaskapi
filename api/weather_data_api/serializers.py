from flask_restplus import fields

from api.restplus import api

humidity = api.model(
    'Humidity',
    {
        'id': fields.Integer(
            readOnly=True,
            description='The unique identifier of the record'),
        'value': fields.Float(
            required=True,
            readOnly=True,
            description='The reading''s value'),
        'value_units': fields.String(
            required=True,
            readOnly=True,
            max=16,
            description='The unit for the value (e.g. percent)'),
        'value_error_range': fields.Float(
            required=True,
            readOnly=True,
            description='The error range for the reading''s value'),
        'latitude': fields.Float(
            required=True,
            readOnly=True,
            description='The latitude of the reading'),
        'longitude': fields.Float(
            required=True,
            readOnly=True,
            description='The longitude of the reading'),
        'elevation': fields.Float(
            required=True,
            readOnly=True,
            description='The record''s elevation.'),
        'elevation_units': fields.String(
            required=True,
            readOnly=True,
            max=16,
            description='The unit for the elevation (e.g. meters, feet)'),
        'timestamp': fields.DateTime(
            required=True,
            readOnly=True,
            description='The date and time the reading was recorded'),
    })

pressure = api.model(
    'Pressure',
    {
        'id': fields.Integer(
            readOnly=True,
            description='The unique identifier of the record'),
        'value': fields.Float(
            required=True,
            readOnly=True,
            description='The reading''s value'),
        'value_units': fields.String(
            required=True,
            readOnly=True,
            max=16,
            description='The unit for the value (e.g. Pa, kPa, psi, atm)'),
        'value_error_range': fields.Float(
            required=True,
            readOnly=True,
            description='The error range for the reading''s value'),
        'latitude': fields.Float(
            required=True,
            readOnly=True,
            description='The latitude of the reading'),
        'longitude': fields.Float(
            required=True,
            readOnly=True,
            description='The longitude of the reading'),
        'elevation': fields.Float(
            required=True,
            readOnly=True,
            description='The record''s elevation.'),
        'elevation_units': fields.String(
            required=True,
            readOnly=True,
            max=16,
            description='The unit for the elevation (e.g. meters, feet)'),
        'timestamp': fields.DateTime(
            required=True,
            readOnly=True,
            description='The date and time the reading was recorded'),
    })

temperature = api.model(
    'Temperature',
    {
        'id': fields.Integer(
            readOnly=True,
            description='The unique identifier of the record'),
        'value': fields.Float(
            required=True,
            readOnly=True,
            description='The reading''s value'),
        'value_units': fields.String(
            required=True,
            readOnly=True,
            max=16,
            description='The unit for the value (e.g. Pa, kPa, psi, atm)'),
        'value_error_range': fields.Float(
            required=True,
            readOnly=True,
            description='The error range for the reading''s value'),
        'latitude': fields.Float(
            required=True,
            readOnly=True,
            description='The latitude of the reading'),
        'longitude': fields.Float(
            required=True,
            readOnly=True,
            description='The longitude of the reading'),
        'elevation': fields.Float(
            required=True,
            readOnly=True,
            description='The record''s elevation.'),
        'elevation_units': fields.String(
            required=True,
            readOnly=True,
            max=16,
            description='The unit for the elevation (e.g. meters, feet)'),
        'timestamp': fields.DateTime(
            required=True,
            readOnly=True,
            description='The date and time the reading was recorded'),
    })
