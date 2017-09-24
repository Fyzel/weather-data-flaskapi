"""
@author:     Fyzel@users.noreply.github.com

@copyright:  2017 Englesh.org. All rights reserved.

@license:    https://github.com/Fyzel/weather-data-flaskapi/blob/master/LICENSE

@contact:    Fyzel@users.noreply.github.com
@deffield    updated: 2017-06-14
"""

import decimal
from datetime import datetime

from database import db
from database.model_exceptions import LatitudeValueError, LongitudeValueError


class Humidity(db.Model):
    """
    A class that represents the ORM for a humidity reading.
    """
    __tablename__ = 'humidities'
    id = db.Column(db.BIGINT(), primary_key=True, autoincrement=True)
    value = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    value_units = db.Column(db.NVARCHAR(16), nullable=False)
    value_error_range = db.Column(db.DECIMAL(precision=7, scale=6), nullable=False, default=0.0)
    latitude = db.Column(db.DECIMAL(precision=8, scale=6), nullable=False)
    longitude = db.Column(db.DECIMAL(precision=9, scale=6), nullable=False)
    elevation = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    elevation_units = db.Column(db.NVARCHAR(16), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,
                 value: decimal,
                 value_units: str,
                 value_error_range: decimal,
                 latitude: decimal,
                 longitude: decimal,
                 elevation: decimal,
                 elevation_units: str,
                 timestamp: datetime,
                 id=None):
        """
        Humidity constructor.

        Latitude -90 to 90. Longitude -180 to 180.

        :rtype: Humidity
        :type value: decimal
        :type value_units: str
        :type value_error_range: decimal
        :type latitude: decimal
        :type longitude: decimal
        :type elevation: decimal
        :type elevation_units: str
        :type timestamp: datetime
        """
        super().__init__()

        # Test case for latitude and longitude value assertions
        if latitude < -90.0 or latitude > 90.0:
            raise LatitudeValueError('latitude out of range (-90 to 90)')

        if longitude < -180.0 or longitude > 180:
            raise LongitudeValueError('longitude out of range (-90 to 90)')

        if id is not None:
            self.id = id

        self.value = value
        self.value_units = value_units
        self.value_error_range = value_error_range
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.elevation_units = elevation_units
        self.timestamp = timestamp

    def __repr__(self):
        """
        Return a string representation of the Humidity object.

        :return: A string representation of the Humidity object.
        """
        if self.id is None:
            # for python 3.5
            return '<Humidity: value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '           timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '           latitude: {latitude:f}\n' + \
                   '           longitude: {longitude:f}>\n' + \
                   '           elevation: {elevation:f} {elevation_units}>'.format(
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude=self.latitude,
                       longitude=self.longitude,
                       elevation=self.elevation,
                       elevation_units=self.elevation_units
                   )
            # for python 3.6
            # return (f'<Humidity: value: {self.value:f} {self.value_units} +/- {self.value_error_range:.2%}\n'
            #         f'           timestamp: {self.timestamp:%Y-%m-%d %H:%M:%S}\n'
            #         f'           latitude: {self.latitude:f}\n'
            #         f'           longitude: {self.longitude:f}>\n'
            #         f'           elevation: {self.elevation:f} {self.elevation_units}>\n')
        else:
            # for python 3.5
            return '<Humidity: id: {id)}\n' + \
                   '           value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '           timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '           latitude: {latitude:f}\n' + \
                   '           longitude: {longitude:f}>\n' + \
                   '           elevation: {elevation:f} {elevation_units}>\n'.format(
                       id=str(self.id),
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude=self.latitude,
                       longitude=self.longitude,
                       elevation=self.elevation,
                       elevation_units=self.elevation_units
                   )
            # for python 3.6
            # return (f'<Humidity: id: {str(self.id)}\n'
            #         f'           value: {self.value:f} {self.value_units} +/- {self.value_error_range:.2%}\n'
            #         f'           timestamp: {self.timestamp:%Y-%m-%d %H:%M:%S}\n'
            #         f'           latitude: {self.latitude:f}\n'
            #         f'           longitude: {self.longitude:f}>\n'
            #         f'           elevation: {self.elevation:f} {self.elevation_units}>\n')

    def __str__(self):
        return self.__repr__()


class Pressure(db.Model):
    """
    A class that represents the ORM for a pressure reading.
    """
    __tablename__ = 'pressures'
    id = db.Column(db.BIGINT(), primary_key=True, autoincrement=True)
    value = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    value_units = db.Column(db.NVARCHAR(16), nullable=False)
    value_error_range = db.Column(db.DECIMAL(precision=7, scale=6), nullable=False, default=0.0)
    latitude = db.Column(db.DECIMAL(precision=8, scale=6), nullable=False)
    longitude = db.Column(db.DECIMAL(precision=9, scale=6), nullable=False)
    elevation = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    elevation_units = db.Column(db.NVARCHAR(16), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,
                 value: decimal,
                 value_units: str,
                 value_error_range: decimal,
                 latitude: decimal,
                 longitude: decimal,
                 elevation: decimal,
                 elevation_units: str,
                 timestamp: datetime,
                 id=None):
        """
        Pressure constructor.

        Latitude -90 to 90. Longitude -180 to 180.

        :rtype: Pressure
        :type value: decimal
        :type value_units: str
        :type value_error_range: decimal
        :type latitude: decimal
        :type longitude: decimal
        :type elevation: decimal
        :type elevation_units: str
        :type timestamp: datetime
        """
        super().__init__()

        # Pressure: Test case for latitude and longitude value assertions
        if latitude < -90.0 or latitude > 90.0:
            raise LatitudeValueError('latitude out of range (-90 to 90)')

        if longitude < -180.0 or longitude > 180:
            raise LongitudeValueError('longitude out of range (-90 to 90)')

        if id is not None:
            self.id = id

        self.value = value
        self.value_units = value_units
        self.value_error_range = value_error_range
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.elevation_units = elevation_units
        self.timestamp = timestamp

    def __repr__(self) -> str:
        """
        Return a string representation of the Pressure object.

        :return: A string representation of the Pressure object.
        """
        if self.id is None:
            # for python 3.5
            return '<Pressure: value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '           timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '           latitude: {latitude:f}\n' + \
                   '           longitude: {longitude:f}>\n' + \
                   '           elevation: {elevation:f} {elevation_units}>\n'.format(
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude=self.latitude,
                       longitude=self.longitude,
                       elevation=self.elevation,
                       elevation_units=self.elevation_units
                   )
            # for python 3.6
            # return (f'<Pressure: value: {self.value:f} {self.value_units} +/- {self.value_error_range:.2%}\n'
            #         f'           timestamp: {self.timestamp:%Y-%m-%d %H:%M:%S}\n'
            #         f'           latitude: {self.latitude:f}\n'
            #         f'           longitude: {self.longitude:f}>\n'
            #         f'           elevation: {self.elevation:f} {self.elevation_units}>\n')
        else:
            # for python 3.5
            return '<Pressure: id: {id}\n' + \
                   '           value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '           timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '           latitude: {latitude:f}\n' + \
                   '           longitude: {longitude:f}>\n' + \
                   '           elevation: {elevation:f} {elevation_units}>\n'.format(
                       id=str(self.id),
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude=self.latitude,
                       longitude=self.longitude,
                       elevation=self.elevation,
                       elevation_units=self.elevation_units
                   )
            # for python 3.6
            # return (f'<Pressure: id: {str(self.id)}\n'
            #         f'           value: {self.value:f} {self.value_units} +/- {self.value_error_range:.2%}\n'
            #         f'           timestamp: {self.timestamp:%Y-%m-%d %H:%M:%S}\n'
            #         f'           latitude: {self.latitude:f}\n'
            #         f'           longitude: {self.longitude:f}>\n'
            #         f'           elevation: {self.elevation:f} {self.elevation_units}>\n')

    def __str__(self):
        return self.__repr__()


class Temperature(db.Model):
    """
    A class that represents the ORM for a temperature reading.
    """
    __tablename__ = 'temperatures'
    id = db.Column(db.BIGINT(), primary_key=True, autoincrement=True)
    value = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    value_units = db.Column(db.NVARCHAR(16), nullable=False)
    value_error_range = db.Column(db.DECIMAL(precision=7, scale=6), nullable=False, default=0.0)
    latitude = db.Column(db.DECIMAL(precision=8, scale=6), nullable=False)
    longitude = db.Column(db.DECIMAL(precision=9, scale=6), nullable=False)
    elevation = db.Column(db.DECIMAL(precision=8, scale=4), nullable=False)
    elevation_units = db.Column(db.NVARCHAR(16), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def __init__(self,
                 value: decimal,
                 value_units: str,
                 value_error_range: decimal,
                 latitude: decimal,
                 longitude: decimal,
                 elevation: decimal,
                 elevation_units: str,
                 timestamp: datetime,
                 id=None):
        """
        Temperature constructor.

        Latitude -90 to 90. Longitude -180 to 180.

        :rtype: Temperature
        :type value: decimal
        :type value_units: str
        :type value_error_range: decimal
        :type latitude: decimal
        :type longitude: decimal
        :type elevation: decimal
        :type elevation_units: str
        :type timestamp: datetime
        :param id: The unique identifier
        :type id: int
        """
        super().__init__()

        # Test case for latitude and longitude value assertions
        if latitude < -90.0 or latitude > 90.0:
            raise LatitudeValueError('latitude out of range (-90 to 90)')

        if longitude < -180.0 or longitude > 180:
            raise LongitudeValueError('longitude out of range (-90 to 90)')

        if id is not None:
            self.id = id

        self.value = value
        self.value_units = value_units
        self.value_error_range = value_error_range
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.elevation_units = elevation_units
        self.timestamp = timestamp

    def __repr__(self) -> str:
        """
        Return a string representation of the Temperature object.

        :return: A string representation of the Temperature object.
        """
        if self.id is None:
            # for python 3.5
            return '<Temperature: value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '              timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '              latitude: {latitude:f}\n' + \
                   '              longitude: {longitude:f}>\n' + \
                   '              elevation: {elevation:f} {elevation_units}>'.format(
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude=self.latitude,
                       longitude=self.longitude,
                       elevation=self.elevation,
                       elevation_units=self.elevation_units
                   )
            # for python 3.6
            # return (f'<Temperature: value: {self.value:f} {self.value_units} +/- {self.value_error_range:.2%}\n'
            #         f'              timestamp: {self.timestamp:%Y-%m-%d %H:%M:%S}\n'
            #         f'              latitude: {self.latitude:f}\n'
            #         f'              longitude: {self.longitude:f}>')
        else:
            # for python 3.5
            return '<Temperature: id: {id}\n' + \
                   '              value: {value:f} {value_units} +/- {value_error_range:.2%}\n' + \
                   '              timestamp: {timestamp:%Y-%m-%d %H:%M:%S}\n' + \
                   '              latitude: {latitude:f}\n' + \
                   '              longitude: {longitude:f}>' + \
                   '              elevation: {elevation:f} {elevation_units}>\n'.format(
                       id=str(self.id),
                       value=self.value,
                       value_units=self.value_units,
                       value_error_range=self.value_error_range,
                       timestamp=self.timestamp,
                       latitude=self.latitude,
                       longitude=self.longitude,
                       elevation=self.elevation,
                       elevation_units=self.elevation_units
                   )
            # for python 3.6
            # return (f'<Temperature: id: {str(self.id)}\n'
            #         f'              value: {self.value:f} {self.value_units} +/- {self.value_error_range:.2%}\n'
            #         f'              timestamp: {self.timestamp:%Y-%m-%d %H:%M:%S}\n'
            #         f'              latitude: {self.latitude:f}\n'
            #         f'              longitude: {self.longitude:f}>')

    def __str__(self):
        return self.__repr__()


class User(db.Model):
    """
    A class that represents the ORM for a user account.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.NVARCHAR(64), nullable=False)
    password = db.Column(db.NVARCHAR(120), nullable=False)
    enabled = db.Column(db.BOOLEAN, nullable=False)
    created_date = db.Column(db.DATETIME, nullable=False, default=datetime.utcnow())
    last_login_date = db.Column(db.DATETIME, nullable=True)

    def __init__(self,
                 username: str,
                 password: str,
                 enabled: bool,
                 created_date: datetime = None,
                 last_login_date: datetime = None,
                 id=None):
        """
        User constructor.

        :param username: The user's username.
        :type username: str
        :param password: The user's SHA256 encrypted password.
        :type password: str
        :param enabled: Boolean indicating if the user is enabled for login.
        :type enabled: bool
        :param created_date: The date and time the user's account was created.
        :type created_date: datetime
        :param last_login_date: The date and time the user last logged in.
        :type last_login_date: datetime
        :param id: The database id for the user.
        :type id: int
        """
        super().__init__()

        if id is not None:
            self.id = id
        self.username = username
        self.password = password
        self.enabled = enabled
        self.created_date = created_date
        self.last_login_date = last_login_date

    def __repr__(self) -> str:
        """
        Return a string representation of the User object.

        :return: A string representation of the User object.
        """
        result = '<User: id: {id} username: {username}>'.format(
            id=str(self.id),
            username=self.username
        )
        return result

    def __str__(self):
        result = self.__repr__()
        return result
