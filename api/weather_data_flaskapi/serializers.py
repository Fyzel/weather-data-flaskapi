"""
@author:     Fyzel@users.noreply.github.com

@copyright:  2017 Englesh.org. All rights reserved.

@license:    https://github.com/Fyzel/weather-data-flaskapi/blob/master/LICENSE

@contact:    Fyzel@users.noreply.github.com
@deffield    updated: 2017-06-14
"""

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
        'latitude_public': fields.Float(
            required=True,
            readOnly=True,
            description='The public latitude of the reading'),
        'longitude': fields.Float(
            required=True,
            readOnly=True,
            description='The longitude of the reading'),
        'longitude_public': fields.Float(
            required=True,
            readOnly=True,
            description='The public longitude of the reading'),
        'city': fields.String(
            required=True,
            readOnly=True,
            description='The record''s city.'),
        'province': fields.String(
            required=True,
            readOnly=True,
            description='The record''s province.'),
        'country': fields.String(
            required=True,
            readOnly=True,
            description='The record''s country.'),
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

public_humidity = api.model(
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
        'latitude_public': fields.Float(
            required=True,
            readOnly=True,
            description='The public latitude of the reading'),
        'longitude_public': fields.Float(
            required=True,
            readOnly=True,
            description='The public longitude of the reading'),
        'city': fields.String(
            required=True,
            readOnly=True,
            description='The record''s city.'),
        'province': fields.String(
            required=True,
            readOnly=True,
            description='The record''s province.'),
        'country': fields.String(
            required=True,
            readOnly=True,
            description='The record''s country.'),
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
            description='The unit for the value (e.g. percent)'),
        'value_error_range': fields.Float(
            required=True,
            readOnly=True,
            description='The error range for the reading''s value'),
        'latitude': fields.Float(
            required=True,
            readOnly=True,
            description='The latitude of the reading'),
        'latitude_public': fields.Float(
            required=True,
            readOnly=True,
            description='The public latitude of the reading'),
        'longitude': fields.Float(
            required=True,
            readOnly=True,
            description='The longitude of the reading'),
        'longitude_public': fields.Float(
            required=True,
            readOnly=True,
            description='The public longitude of the reading'),
        'city': fields.String(
            required=True,
            readOnly=True,
            description='The record''s city.'),
        'province': fields.String(
            required=True,
            readOnly=True,
            description='The record''s province.'),
        'country': fields.String(
            required=True,
            readOnly=True,
            description='The record''s country.'),
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

public_pressure = api.model(
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
            description='The unit for the value (e.g. percent)'),
        'value_error_range': fields.Float(
            required=True,
            readOnly=True,
            description='The error range for the reading''s value'),
        'latitude_public': fields.Float(
            required=True,
            readOnly=True,
            description='The public latitude of the reading'),
        'longitude_public': fields.Float(
            required=True,
            readOnly=True,
            description='The public longitude of the reading'),
        'city': fields.String(
            required=True,
            readOnly=True,
            description='The record''s city.'),
        'province': fields.String(
            required=True,
            readOnly=True,
            description='The record''s province.'),
        'country': fields.String(
            required=True,
            readOnly=True,
            description='The record''s country.'),
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
            description='The unit for the value (e.g. percent)'),
        'value_error_range': fields.Float(
            required=True,
            readOnly=True,
            description='The error range for the reading''s value'),
        'latitude': fields.Float(
            required=True,
            readOnly=True,
            description='The latitude of the reading'),
        'latitude_public': fields.Float(
            required=True,
            readOnly=True,
            description='The public latitude of the reading'),
        'longitude': fields.Float(
            required=True,
            readOnly=True,
            description='The longitude of the reading'),
        'longitude_public': fields.Float(
            required=True,
            readOnly=True,
            description='The public longitude of the reading'),
        'city': fields.String(
            required=True,
            readOnly=True,
            description='The record''s city.'),
        'province': fields.String(
            required=True,
            readOnly=True,
            description='The record''s province.'),
        'country': fields.String(
            required=True,
            readOnly=True,
            description='The record''s country.'),
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

public_temperature = api.model(
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
            description='The unit for the value (e.g. percent)'),
        'value_error_range': fields.Float(
            required=True,
            readOnly=True,
            description='The error range for the reading''s value'),
        'latitude_public': fields.Float(
            required=True,
            readOnly=True,
            description='The public latitude of the reading'),
        'longitude_public': fields.Float(
            required=True,
            readOnly=True,
            description='The public longitude of the reading'),
        'city': fields.String(
            required=True,
            readOnly=True,
            description='The record''s city.'),
        'province': fields.String(
            required=True,
            readOnly=True,
            description='The record''s province.'),
        'country': fields.String(
            required=True,
            readOnly=True,
            description='The record''s country.'),
        'timestamp': fields.DateTime(
            required=True,
            readOnly=True,
            description='The date and time the reading was recorded'),
    })
