"""
@author:     Fyzel@users.noreply.github.com

@copyright:  2017 Englesh.org. All rights reserved.

@license:    https://github.com/Fyzel/weather-data-flaskapi/blob/master/LICENSE

@contact:    Fyzel@users.noreply.github.com
@deffield    updated: 2017-06-14
"""

from database import db
from database.models import Humidity, Pressure, Temperature


def create_humidity(data) -> Humidity:
    """
    Creates a new humidity record in the database.

    :param data: JSON data for a new Humidity object.
    :return: Humidity
    """
    value = data.get('value')
    value_units = data.get('value_units')
    value_error_range = data.get('value_error_range')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    city = data.get('city')
    province = data.get('province')
    country = data.get('country')
    elevation = data.get('elevation')
    elevation_units = data.get('elevation_units')
    timestamp = data.get('timestamp')

    humidity = Humidity(value=value,
                        value_units=value_units,
                        value_error_range=value_error_range,
                        latitude=latitude,
                        longitude=longitude,
                        city=city,
                        province=province,
                        country=country,
                        elevation=elevation,
                        elevation_units=elevation_units,
                        timestamp=timestamp)

    db.session.add(humidity)
    db.session.commit()

    return humidity


def update_humidity(humidity_id: int, data) -> Humidity:
    """
    Update a humidity record in the database.

    :param humidity_id: The humidity record identifier.
    :param data: Updated JSON data for an existing Humidity object.
    :return: Humidity
    """
    humidity = Humidity.query.filter(Humidity.id == humidity_id).one()
    humidity.value = data.get('value')
    humidity.value_units = data.get('value_units')
    humidity.value_error_range = data.get('value_error_range')
    humidity.latitude = data.get('latitude')
    humidity.latitude_public_public = float(int(humidity.latitude * 1000)) / 1000
    humidity.longitude = data.get('longitude')
    humidity.longitude_public = float(int(humidity.longitude * 1000)) / 1000
    humidity.city = data.get('city')
    humidity.province = data.get('province')
    humidity.country = data.get('country')
    humidity.elevation = data.get('elevation')
    humidity.elevation_units = data.get('elevation_units')
    humidity.timestamp = data.get('timestamp')

    db.session.add(humidity)
    db.session.commit()

    return humidity


def delete_humidity(humidity_id: int):
    """
    Delete a humidity record in the database.

    :param humidity_id: The humidity record identifier.
    :return: None
    """
    humidity = Humidity.query.filter(Humidity.id == humidity_id).one()
    db.session.delete(humidity)
    db.session.commit()


def create_pressure(data) -> Pressure:
    """
    Creates a new pressure record in the database.

    :param data: JSON data for a new Pressure object.
    :return: Pressure
    """
    value = data.get('value')
    value_units = data.get('value_units')
    value_error_range = data.get('value_error_range')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    city = data.get('city')
    province = data.get('province')
    country = data.get('country')
    elevation = data.get('elevation')
    elevation_units = data.get('elevation_units')
    timestamp = data.get('timestamp')

    pressure = Pressure(value=value,
                        value_units=value_units,
                        value_error_range=value_error_range,
                        latitude=latitude,
                        longitude=longitude,
                        city=city,
                        province=province,
                        country=country,
                        elevation=elevation,
                        elevation_units=elevation_units,
                        timestamp=timestamp)

    db.session.add(pressure)
    db.session.commit()

    return pressure


def update_pressure(pressure_id: int, data) -> Pressure:
    """
    Update a pressure record in the database.

    :param pressure_id: The pressure record identifier.
    :param data: Updated JSON data for an existing Pressure object.
    :return: Pressure
    """
    pressure = Pressure.query.filter(Pressure.id == pressure_id).one()
    pressure.value = data.get('value')
    pressure.value_units = data.get('value_units')
    pressure.value_error_range = data.get('value_error_range')
    pressure.latitude = data.get('latitude')
    pressure.latitude_public_public = float(int(pressure.latitude * 1000)) / 1000
    pressure.longitude = data.get('longitude')
    pressure.longitude_public = float(int(pressure.longitude * 1000)) / 1000
    pressure.city = data.get('city')
    pressure.province = data.get('province')
    pressure.country = data.get('country')
    pressure.elevation = data.get('elevation')
    pressure.elevation_units = data.get('elevation_units')
    pressure.timestamp = data.get('timestamp')

    db.session.add(pressure)
    db.session.commit()

    return pressure


def delete_pressure(pressure_id: int):
    """
    Delete a pressure record in the database.

    :param pressure_id: The pressure record identifier.
    :return: None
    """
    pressure = Pressure.query.filter(Pressure.id == pressure_id).one()
    db.session.delete(pressure)
    db.session.commit()


def create_temperature(data) -> Temperature:
    """
    Creates a new temperature record in the database.

    :param data: JSON data for a new Temperature object.
    :return: Temperature
    """
    value = data.get('value')
    value_units = data.get('value_units')
    value_error_range = data.get('value_error_range')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    city = data.get('city')
    province = data.get('province')
    country = data.get('country')
    elevation = data.get('elevation')
    elevation_units = data.get('elevation_units')
    timestamp = data.get('timestamp')

    temperature = Temperature(value=value,
                              value_units=value_units,
                              value_error_range=value_error_range,
                              latitude=latitude,
                              longitude=longitude,
                              city=city,
                              province=province,
                              country=country,
                              elevation=elevation,
                              elevation_units=elevation_units,
                              timestamp=timestamp)

    db.session.add(temperature)
    db.session.commit()

    return temperature


def update_temperature(temperature_id: int, data) -> Temperature:
    """
    Update a temperature record in the database.

    :param temperature_id: The temperature record identifier.
    :param data: Updated JSON data for an existing Temperature object.
    :return: Temperature
    """
    temperature = Temperature.query.filter(Temperature.id == temperature_id).one()
    temperature.value = data.get('value')
    temperature.value_units = data.get('value_units')
    temperature.value_error_range = data.get('value_error_range')
    temperature.latitude = data.get('latitude')
    temperature.latitude_public_public = float(int(temperature.latitude * 1000)) / 1000
    temperature.longitude = data.get('longitude')
    temperature.longitude_public = float(int(temperature.longitude * 1000)) / 1000
    temperature.city = data.get('city')
    temperature.province = data.get('province')
    temperature.country = data.get('country')
    temperature.timestamp = data.get('timestamp')
    temperature.elevation = data.get('elevation')
    temperature.elevation_units = data.get('elevation_units')

    db.session.add(temperature)
    db.session.commit()

    return temperature


def delete_temperature(temperature_id: int):
    """
    Delete a temperature record in the database.

    :param temperature_id: The temperature record identifier.
    :return: None
    """
    temperature = Temperature.query.filter(Temperature.id == temperature_id).one()
    db.session.delete(temperature)
    db.session.commit()
