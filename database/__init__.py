"""
@author:     Fyzel@users.noreply.github.com

@copyright:  2017 Englesh.org. All rights reserved.

@license:    https://github.com/Fyzel/weather-data-flaskapi/blob/master/LICENSE

@contact:    Fyzel@users.noreply.github.com
@deffield    updated: 2017-06-14
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_humidity_indexes(app):
    with app.app_context():
        from sqlalchemy import text
        from sqlalchemy.exc import OperationalError

        # Create humidity table indices
        try:
            sql = text(
                'CREATE UNIQUE INDEX humidity_city_subdivision_country_index ON humidity (city, subdivision, country);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX humidity_city_index ON humidity (city);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX humidity_subdivision_index ON humidity (subdivision);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX humidity_country_index ON humidity (country);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX humidity_latitude_longitude_index ON humidity (latitude, longitude);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX humidity_timestamp_index ON humidity (timestamp);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass


def create_pressure_indexes(app):
    with app.app_context():
        from sqlalchemy import text
        from sqlalchemy.exc import OperationalError

        # Create pressure table indices
        try:
            sql = text(
                'CREATE UNIQUE INDEX pressure_city_subdivision_country_index ON pressure (city, subdivision, country);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX pressure_city_index ON pressure (city);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX pressure_subdivision_index ON pressure (subdivision);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX pressure_country_index ON pressure (country);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX pressure_latitude_longitude_index ON pressure (latitude, longitude);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX pressure_timestamp_index ON pressure (timestamp);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass


def create_temperature_indexes(app):
    with app.app_context():
        from sqlalchemy import text
        from sqlalchemy.exc import OperationalError

        # Create temperature table indices
        try:
            sql = text(
                'CREATE UNIQUE INDEX temperature_city_subdivision_country_index ON temperature (city, subdivision, country);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX temperature_city_index ON temperature (city);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX temperature_subdivision_index ON temperature (subdivision);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX temperature_country_index ON temperature (country);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX temperature_latitude_longitude_index ON temperature (latitude, longitude);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass

        try:
            sql = text('CREATE INDEX temperature_timestamp_index ON temperature (timestamp);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass


def create_user_indexes(app):
    with app.app_context():
        from sqlalchemy import text
        from sqlalchemy.exc import OperationalError

        # Create user table indices
        try:
            sql = text('CREATE INDEX user_username_index ON user (username);')
            db.engine.execute(sql)
        except OperationalError as oe:
            pass


def create_indexes(app):
    create_humidity_indexes(app)
    create_pressure_indexes(app)
    create_temperature_indexes(app)
    create_user_indexes(app)


def create_database(app=None):
    db.create_all(app=app)
    create_indexes(app)


def reset_database():
    from database.models import ProtectedHumidity, ProtectedPressure, ProtectedTemperature, User
    db.drop_all()
    db.create_all()
