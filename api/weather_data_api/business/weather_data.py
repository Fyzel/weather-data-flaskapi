from database import db
from database.models import ProtectedHumidity, ProtectedPressure, ProtectedTemperature


def create_humidity(data) -> ProtectedHumidity:
    """
    Creates a new humidity record in the database.

    :param data: JSON data for a new ProtectedHumidity object.
    :return: ProtectedHumidity
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

    humidity = ProtectedHumidity(value=value,
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


def update_humidity(humidity_id: int, data) -> ProtectedHumidity:
    """
    Update a humidity record in the database.

    :param humidity_id: The humidity record identifier.
    :param data: Updated JSON data for an existing ProtectedHumidity object.
    :return: ProtectedHumidity
    """
    humidity = ProtectedHumidity.query.filter(ProtectedHumidity.id == humidity_id).one()
    humidity.value = data.get('value')
    humidity.value_units = data.get('value_units')
    humidity.value_error_range = data.get('value_error_range')
    humidity.latitude = data.get('latitude')
    humidity.longitude = data.get('longitude')
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
    humidity = ProtectedHumidity.query.filter(ProtectedHumidity.id == humidity_id).one()
    db.session.delete(humidity)
    db.session.commit()


def create_pressure(data) -> ProtectedPressure:
    """
    Creates a new pressure record in the database.

    :param data: JSON data for a new ProtectedPressure object.
    :return: ProtectedPressure
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

    pressure = ProtectedPressure(value=value,
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


def update_pressure(pressure_id: int, data) -> ProtectedPressure:
    """
    Update a pressure record in the database.

    :param pressure_id: The pressure record identifier.
    :param data: Updated JSON data for an existing ProtectedPressure object.
    :return: ProtectedPressure
    """
    pressure = ProtectedPressure.query.filter(ProtectedPressure.id == pressure_id).one()
    pressure.value = data.get('value')
    pressure.value_units = data.get('value_units')
    pressure.value_error_range = data.get('value_error_range')
    pressure.latitude = data.get('latitude')
    pressure.longitude = data.get('longitude')
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
    pressure = ProtectedPressure.query.filter(ProtectedPressure.id == pressure_id).one()
    db.session.delete(pressure)
    db.session.commit()


def create_temperature(data) -> ProtectedTemperature:
    """
    Creates a new temperature record in the database.

    :param data: JSON data for a new ProtectedTemperature object.
    :return: ProtectedTemperature
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

    temperature = ProtectedTemperature(value=value,
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


def update_temperature(temperature_id: int, data) -> ProtectedTemperature:
    """
    Update a temperature record in the database.

    :param temperature_id: The temperature record identifier.
    :param data: Updated JSON data for an existing ProtectedTemperature object.
    :return: ProtectedTemperature
    """
    temperature = ProtectedTemperature.query.filter(ProtectedTemperature.id == temperature_id).one()
    temperature.value = data.get('value')
    temperature.value_units = data.get('value_units')
    temperature.value_error_range = data.get('value_error_range')
    temperature.latitude = data.get('latitude')
    temperature.longitude = data.get('longitude')
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
    temperature = ProtectedTemperature.query.filter(ProtectedTemperature.id == temperature_id).one()
    db.session.delete(temperature)
    db.session.commit()
