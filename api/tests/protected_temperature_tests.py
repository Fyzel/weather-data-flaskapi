"""
@author:     Fyzel@users.noreply.github.com

@copyright:  2017 Englesh.org. All rights reserved.

@license:    https://github.com/Fyzel/weather-data-flaskapi/blob/master/LICENSE

@contact:    Fyzel@users.noreply.github.com
@deffield    updated: 2017-06-14
"""

import json
import logging
import random
import sys
import string
import unittest
from datetime import datetime

import pytz
import requests


def get_random_datetime():
    """Return a random datetime from 0001-01-01 00:00:00.0 to 9999-12-28 23:59:59.999999"""
    year = random.randint(1, datetime.now().year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    return datetime(year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute,
                    second=second,
                    tzinfo=pytz.UTC)


def get_random_string(length: int) -> str:
    """Generate a random string of length.

    :arg length: The length of the string
    :rtype str
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def get_random_record_data():
    """Generate a random temperature data record"""
    value = float('{:.4f}'.format(random.uniform(0, 100.0)))
    value_units = get_random_string(16)
    value_error_range = float('{:.6f}'.format(random.uniform(0.0, 1.0)))
    timestamp = get_random_datetime()
    latitude = float('{:.6f}'.format(random.uniform(-90.0, 90.0)))
    longitude = float('{:.6f}'.format(random.uniform(-180.0, 180.0)))
    elevation = float('{:.4f}'.format(random.uniform(-90.0, 999.0)))
    elevation_units = get_random_string(16)
    city = get_random_string(64)
    province = get_random_string(64)
    country = get_random_string(64)

    return {
        'value': value,
        'value_units': value_units,
        'value_error_range': value_error_range,
        'latitude': latitude,
        'longitude': longitude,
        'elevation': elevation,
        'elevation_units': elevation_units,
        'timestamp': timestamp,
        'city': city,
        'province': province,
        'country': country
    }


class TestCaseProtectedTemperature(unittest.TestCase):
    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    @property
    def previous_record(self):
        return self._previous_record

    @previous_record.setter
    def previous_record(self, value):
        self._previous_record = value

    @property
    def last_id(self):
        return self._last_id

    @last_id.setter
    def last_id(self, value: int):
        self._last_id = value

    def setUp(self):
        """
        Configure these to target the environment being tested. Sample values provided.
        """
        self.base_url = 'http://localhost:8888'
        self.context = 'weather'
        self.resource = 'ProtectedTemperatureData'
        self.username = 'admin'
        self.password = 'secret'
        self._token = None
        self._last_id = None

    def tearDown(self):
        pass

    def test_step_00_login_fail(self):
        """Test the login fail capability"""
        log = logging.getLogger("TestCase.test_step_00_login_fail")
        log.info('Start')

        auth_url = '{base_url}/auth'.format(
            base_url=self.base_url
        )

        payload = '{{"username": "{username_value}","password": "{password_value}"}}'.format(
            username_value=self.username[::-1],
            password_value=self.password[::-1]
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('auth_url= {url}'.format(url=auth_url))
        log.debug('username= {username}'.format(username=self.username[::-1]))  # reversed username
        log.debug('password= {password}'.format(password=self.password[::-1]))  # reversed password
        log.debug('payload= {payload}'.format(payload=payload))

        headers = {
            'content-type': 'application/json',
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', auth_url, data=payload, headers=headers)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=401)
        )

        assert response.status_code == 401, 'Expected a HTTP status code 401'
        assert len(response.text) > 0, 'Expected data in the response'

        log.debug('response.text= {text}'.format(text=response.text))

        log.info('End')

    def test_step_01_login(self):
        """Test the login capability and setup for the next set of calls"""
        log = logging.getLogger("TestCase.test_step_01_login")
        log.info('Start')

        log.debug("base_url= %r", self.base_url)

        auth_url = '{base_url}/auth'.format(
            base_url=self.base_url
        )

        payload = '{{"username": "{username_value}","password": "{password_value}"}}'.format(
            username_value=self.username,
            password_value=self.password
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('auth_url= {url}'.format(url=auth_url))
        log.debug('username= {username}'.format(username=self.username[::-1]))
        log.debug('password= {password}'.format(password=self.password[::-1]))
        log.debug('payload= {payload}'.format(payload=payload))

        headers = {
            'content-type': 'application/json',
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', auth_url, data=payload, headers=headers)

        assert response.status_code == 200, 'Expected a HTTP status code 200'
        assert len(response.text) > 0, 'Expected data in the response'

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=200)
        )

        log.debug('response.text= {text}'.format(text=response.text))

        json_data = json.loads(response.text)

        assert json_data['access_token'] is not None, 'Access token is not returned'

        TestCaseProtectedTemperature.token = json_data['access_token']

        log.debug('JWT token= {token}'.format(token=self.token))

        log.info('End')

    def test_step_02_create_record_without_auth(self):
        """Create a temperature record without JWT token."""
        log = logging.getLogger("TestCase.test_step_02_create_record_without_auth")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('auth_url= {url}'.format(url=app_url))

        record_data = get_random_record_data()

        payload = '{{\n' \
                  '"value": {value},\n' \
                  '"value_units": "{value_units}",\n' \
                  '"value_error_range": {value_error_range},\n' \
                  '"latitude": {latitude},\n' \
                  '"latitude_public": {latitude_public},\n' \
                  '"longitude": {longitude},\n' \
                  '"longitude_public": {longitude_public},\n' \
                  '"city": "{city}",\n' \
                  '"province": "{province}",\n' \
                  '"country": "{country}",\n' \
                  '"elevation": {elevation},\n' \
                  '"elevation_units": "{elevation_units}",\n' \
                  '"timestamp": "{timestamp}"\n' \
                  '}}'.format(value=record_data['value'],
                              value_units=record_data['value_units'],
                              value_error_range=record_data['value_error_range'],
                              timestamp=str(record_data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')),
                              latitude=record_data['latitude'],
                              latitude_public=float(int(record_data['latitude'] * 1000)) / 1000,
                              longitude=record_data['longitude'],
                              longitude_public=float(int(record_data['longitude'] * 1000)) / 1000,
                              city=record_data['city'],
                              province=record_data['province'],
                              country=record_data['country'],
                              elevation=record_data['elevation'],
                              elevation_units=record_data['elevation_units'])

        log.debug('payload= {payload}'.format(payload=payload))

        headers = {
            'content-type': 'application/json',
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', app_url, data=payload, headers=headers)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=401)
        )

        assert response.status_code == 401, 'Expected a HTTP status code 401'
        assert len(response.text) > 0, 'Expected data in the response'

        log.info('End')

    def test_step_03_create_record_with_auth(self):
        """Create a temperature record with JWT token."""
        log = logging.getLogger("TestCase.test_step_03_create_record_with_auth")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('app_url= {url}'.format(url=app_url))

        record_data = get_random_record_data()

        payload = '{{\n' \
                  '"value": {value},\n' \
                  '"value_units": "{value_units}",\n' \
                  '"value_error_range": {value_error_range},\n' \
                  '"latitude": {latitude},\n' \
                  '"latitude_public": {latitude_public},\n' \
                  '"longitude": {longitude},\n' \
                  '"longitude_public": {longitude_public},\n' \
                  '"city": "{city}",\n' \
                  '"province": "{province}",\n' \
                  '"country": "{country}",\n' \
                  '"elevation": {elevation},\n' \
                  '"elevation_units": "{elevation_units}",\n' \
                  '"timestamp": "{timestamp}"\n' \
                  '}}'.format(value=record_data['value'],
                              value_units=record_data['value_units'],
                              value_error_range=record_data['value_error_range'],
                              timestamp=str(record_data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')),
                              latitude=record_data['latitude'],
                              latitude_public=float(int(record_data['latitude'] * 1000)) / 1000,
                              longitude=record_data['longitude'],
                              longitude_public=float(int(record_data['longitude'] * 1000)) / 1000,
                              city=record_data['city'],
                              province=record_data['province'],
                              country=record_data['country'],
                              elevation=record_data['elevation'],
                              elevation_units=record_data['elevation_units'])

        log.debug('payload= {payload}'.format(payload=payload))

        headers = {
            'content-type': 'application/json',
            'authorization': 'JWT {token}'.format(token=TestCaseProtectedTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', app_url, data=payload, headers=headers)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=201)
        )

        assert response.status_code == 201, 'Expected a HTTP status code 201'
        assert len(response.text) > 0, 'Expected data in the response'

        json_data = json.loads(response.text)

        assert int(json_data['id']) > 0, "Returned id is greater than 0"

        self.assertEqual(
            json_data['value'],
            record_data['value']), 'Returned value is the same'

        self.assertEqual(
            json_data['value_units'],
            record_data['value_units']), 'Returned value_units is the same'

        self.assertEqual(
            json_data['value_error_range'],
            record_data['value_error_range']), 'Returned value_error_range is the same'

        self.assertEqual(
            json_data['timestamp'],
            str(record_data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S'))), 'Returned timestamp is the same'

        self.assertEqual(
            json_data['elevation'],
            record_data['elevation']), 'Returned elevation is the same'

        self.assertEqual(
            json_data['elevation_units'],
            record_data['elevation_units']), 'Returned elevation_units is the same'

        self.assertEqual(
            json_data['latitude'],
            record_data['latitude']), 'Returned latitude is the same'

        self.assertEqual(
            json_data['latitude_public'],
            float(int(record_data['latitude'] * 1000)) / 1000), 'Returned latitude_public is the same'

        self.assertEqual(
            json_data['longitude'],
            record_data['longitude']), 'Returned longitude is the same'

        self.assertEqual(
            json_data['longitude_public'],
            float(int(record_data['longitude'] * 1000)) / 1000), 'Returned longitude_public is the same'

        self.assertEqual(
            json_data['city'],
            record_data['city']), 'Returned city is the same'

        self.assertEqual(
            json_data['province'],
            record_data['province']), 'Returned province is the same'

        self.assertEqual(
            json_data['country'],
            record_data['country']), 'Returned country is the same'

        TestCaseProtectedTemperature.last_id = json_data['id']
        TestCaseProtectedTemperature.previous_record = json_data

        log.info('End')

    def test_step_03_1_create_record_with_auth_out_of_range_latitude(self):
        """Create a temperature record with JWT token but with out of range latitude."""
        log = logging.getLogger("TestCase.test_step_03_1_create_record_with_auth_out_of_range_latitude")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('app_url= {url}'.format(url=app_url))

        record_data = get_random_record_data()

        record_data['latitude'] = -91

        payload = '{{\n' \
                  '"value": {value},\n' \
                  '"value_units": "{value_units}",\n' \
                  '"value_error_range": {value_error_range},\n' \
                  '"latitude": {latitude},\n' \
                  '"latitude_public": {latitude_public},\n' \
                  '"longitude": {longitude},\n' \
                  '"longitude_public": {longitude_public},\n' \
                  '"city": "{city}",\n' \
                  '"province": "{province}",\n' \
                  '"country": "{country}",\n' \
                  '"elevation": {elevation},\n' \
                  '"elevation_units": "{elevation_units}",\n' \
                  '"timestamp": "{timestamp}"\n' \
                  '}}'.format(value=record_data['value'],
                              value_units=record_data['value_units'],
                              value_error_range=record_data['value_error_range'],
                              timestamp=str(record_data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')),
                              latitude=record_data['latitude'],
                              latitude_public=float(int(record_data['latitude'] * 1000)) / 1000,
                              longitude=record_data['longitude'],
                              longitude_public=float(int(record_data['longitude'] * 1000)) / 1000,
                              city=record_data['city'],
                              province=record_data['province'],
                              country=record_data['country'],
                              elevation=record_data['elevation'],
                              elevation_units=record_data['elevation_units'])

        log.debug('payload= {payload}'.format(payload=payload))

        headers = {
            'content-type': 'application/json',
            'authorization': 'JWT {token}'.format(token=TestCaseProtectedTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', app_url, data=payload, headers=headers)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=400)
        )

        assert response.status_code == 400, 'Expected a HTTP status code 400'
        assert len(response.text) > 0, 'Expected data in the response'

        log.info('End')

    def test_step_03_2_create_record_with_auth_out_of_range_latitude(self):
        """Create a temperature record with JWT token but with out of range latitude."""
        log = logging.getLogger("TestCase.test_step_03_2_create_record_with_auth_out_of_range_latitude")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('app_url= {url}'.format(url=app_url))

        record_data = get_random_record_data()

        record_data['latitude'] = 91

        payload = '{{\n' \
                  '"value": {value},\n' \
                  '"value_units": "{value_units}",\n' \
                  '"value_error_range": {value_error_range},\n' \
                  '"latitude": {latitude},\n' \
                  '"latitude_public": {latitude_public},\n' \
                  '"longitude": {longitude},\n' \
                  '"longitude_public": {longitude_public},\n' \
                  '"city": "{city}",\n' \
                  '"province": "{province}",\n' \
                  '"country": "{country}",\n' \
                  '"elevation": {elevation},\n' \
                  '"elevation_units": "{elevation_units}",\n' \
                  '"timestamp": "{timestamp}"\n' \
                  '}}'.format(value=record_data['value'],
                              value_units=record_data['value_units'],
                              value_error_range=record_data['value_error_range'],
                              timestamp=str(record_data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')),
                              latitude=record_data['latitude'],
                              latitude_public=float(int(record_data['latitude'] * 1000)) / 1000,
                              longitude=record_data['longitude'],
                              longitude_public=float(int(record_data['longitude'] * 1000)) / 1000,
                              city=record_data['city'],
                              province=record_data['province'],
                              country=record_data['country'],
                              elevation=record_data['elevation'],
                              elevation_units=record_data['elevation_units'])

        log.debug('payload= {payload}'.format(payload=payload))

        headers = {
            'content-type': 'application/json',
            'authorization': 'JWT {token}'.format(token=TestCaseProtectedTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', app_url, data=payload, headers=headers)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=400)
        )

        assert response.status_code == 400, 'Expected a HTTP status code 400'
        assert len(response.text) > 0, 'Expected data in the response'

        log.info('End')

    def test_step_03_3_create_record_with_auth_out_of_range_longitude(self):
        """Create a temperature record with JWT token but with out of range longitude."""
        log = logging.getLogger("TestCase.test_step_03_3_create_record_with_auth_out_of_range_longitude")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('app_url= {url}'.format(url=app_url))

        record_data = get_random_record_data()

        record_data['longitude'] = -181

        payload = '{{\n' \
                  '"value": {value},\n' \
                  '"value_units": "{value_units}",\n' \
                  '"value_error_range": {value_error_range},\n' \
                  '"latitude": {latitude},\n' \
                  '"latitude_public": {latitude_public},\n' \
                  '"longitude": {longitude},\n' \
                  '"longitude_public": {longitude_public},\n' \
                  '"city": "{city}",\n' \
                  '"province": "{province}",\n' \
                  '"country": "{country}",\n' \
                  '"elevation": {elevation},\n' \
                  '"elevation_units": "{elevation_units}",\n' \
                  '"timestamp": "{timestamp}"\n' \
                  '}}'.format(value=record_data['value'],
                              value_units=record_data['value_units'],
                              value_error_range=record_data['value_error_range'],
                              timestamp=str(record_data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')),
                              latitude=record_data['latitude'],
                              latitude_public=float(int(record_data['latitude'] * 1000)) / 1000,
                              longitude=record_data['longitude'],
                              longitude_public=float(int(record_data['longitude'] * 1000)) / 1000,
                              city=record_data['city'],
                              province=record_data['province'],
                              country=record_data['country'],
                              elevation=record_data['elevation'],
                              elevation_units=record_data['elevation_units'])

        log.debug('payload= {payload}'.format(payload=payload))

        headers = {
            'content-type': 'application/json',
            'authorization': 'JWT {token}'.format(token=TestCaseProtectedTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', app_url, data=payload, headers=headers)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=400)
        )

        assert response.status_code == 400, 'Expected a HTTP status code 400'
        assert len(response.text) > 0, 'Expected data in the response'

        log.info('End')

    def test_step_03_4_create_record_with_auth_out_of_range_longitude(self):
        """Create a temperature record with JWT token but with out of range latitude."""
        log = logging.getLogger("TestCase.test_step_03_4_create_record_with_auth_out_of_range_longitude")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('app_url= {url}'.format(url=app_url))

        record_data = get_random_record_data()

        record_data['longitude'] = 181

        payload = '{{\n' \
                  '"value": {value},\n' \
                  '"value_units": "{value_units}",\n' \
                  '"value_error_range": {value_error_range},\n' \
                  '"latitude": {latitude},\n' \
                  '"latitude_public": {latitude_public},\n' \
                  '"longitude": {longitude},\n' \
                  '"longitude_public": {longitude_public},\n' \
                  '"city": "{city}",\n' \
                  '"province": "{province}",\n' \
                  '"country": "{country}",\n' \
                  '"elevation": {elevation},\n' \
                  '"elevation_units": "{elevation_units}",\n' \
                  '"timestamp": "{timestamp}"\n' \
                  '}}'.format(value=record_data['value'],
                              value_units=record_data['value_units'],
                              value_error_range=record_data['value_error_range'],
                              timestamp=str(record_data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')),
                              latitude=record_data['latitude'],
                              latitude_public=float(int(record_data['latitude'] * 1000)) / 1000,
                              longitude=record_data['longitude'],
                              longitude_public=float(int(record_data['longitude'] * 1000)) / 1000,
                              city=record_data['city'],
                              province=record_data['province'],
                              country=record_data['country'],
                              elevation=record_data['elevation'],
                              elevation_units=record_data['elevation_units'])

        log.debug('payload= {payload}'.format(payload=payload))

        headers = {
            'content-type': 'application/json',
            'authorization': 'JWT {token}'.format(token=TestCaseProtectedTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', app_url, data=payload, headers=headers)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=400)
        )

        assert response.status_code == 400, 'Expected a HTTP status code 400'
        assert len(response.text) > 0, 'Expected data in the response'

        log.info('End')

    def test_step_04_get_record_without_auth(self):
        """Get a temperature record without JWT token."""
        log = logging.getLogger("TestCase.test_step_04_get_record_without_auth")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/{last_id}'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource,
            last_id=TestCaseProtectedTemperature.last_id
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('app_url= {url}'.format(url=app_url))

        headers = {
            'cache-control': 'no-cache'
        }

        response = requests.request('GET', app_url, headers=headers)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=401)
        )

        assert response.status_code == 401, 'Expected a HTTP status code 401'

        log.info('End')

    def test_step_05_get_record_with_auth(self):
        """Get a temperature record with JWT token."""
        log = logging.getLogger("TestCase.test_step_05_get_record_with_auth")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/{last_id}'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource,
            last_id=TestCaseProtectedTemperature.last_id
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('app_url= {url}'.format(url=app_url))

        headers = {
            'authorization': 'JWT {token}'.format(token=TestCaseProtectedTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('GET', app_url, headers=headers)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=200)
        )

        assert response.status_code == 200, 'Expected a HTTP status code 200'

        json_data = json.loads(response.text)

        self.assertEqual(
            int(json_data['id']),
            int(TestCaseProtectedTemperature.last_id)), "Returned id is the same"

        self.assertEqual(
            json_data['value'],
            TestCaseProtectedTemperature.previous_record['value']), 'Returned value is the same'

        self.assertEqual(
            json_data['value_units'],
            TestCaseProtectedTemperature.previous_record['value_units']), 'Returned value_units is the same'

        self.assertEqual(
            json_data['value_error_range'],
            TestCaseProtectedTemperature.previous_record['value_error_range']), 'Returned value_error_range is the same'

        self.assertEqual(
            json_data['timestamp'],
            TestCaseProtectedTemperature.previous_record['timestamp']), 'Returned timestamp is the same'

        self.assertEqual(
            json_data['elevation'],
            TestCaseProtectedTemperature.previous_record['elevation']), 'Returned elevation is the same'

        self.assertEqual(
            json_data['elevation_units'],
            TestCaseProtectedTemperature.previous_record['elevation_units']), 'Returned elevation_units is the same'

        self.assertEqual(
            json_data['latitude'],
            TestCaseProtectedTemperature.previous_record['latitude']), 'Returned latitude is the same'

        self.assertEqual(
            json_data['latitude_public'],
            TestCaseProtectedTemperature.previous_record['latitude_public']), 'Returned latitude_public is the same'

        self.assertEqual(
            json_data['longitude'],
            TestCaseProtectedTemperature.previous_record['longitude']), 'Returned longitude is the same'

        self.assertEqual(
            json_data['longitude_public'],
            TestCaseProtectedTemperature.previous_record['longitude_public']), 'Returned longitude_public is the same'

        self.assertEqual(
            json_data['city'],
            TestCaseProtectedTemperature.previous_record['city']), 'Returned city is the same'

        self.assertEqual(
            json_data['province'],
            TestCaseProtectedTemperature.previous_record['province']), 'Returned province is the same'

        self.assertEqual(
            json_data['country'],
            TestCaseProtectedTemperature.previous_record['country']), 'Returned country is the same'

        log.info('End')

    def test_step_06_update_record_without_auth(self):
        """Update a temperature record without JWT token."""
        log = logging.getLogger("TestCase.test_step_06_update_record_without_auth")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/{last_id}'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource,
            last_id=TestCaseProtectedTemperature.last_id
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('app_url= {url}'.format(url=app_url))

        record_data = get_random_record_data()

        payload = '{{\n' \
                  '"value": {value},\n' \
                  '"value_units": "{value_units}",\n' \
                  '"value_error_range": {value_error_range},\n' \
                  '"latitude": {latitude},\n' \
                  '"latitude_public": {latitude_public},\n' \
                  '"longitude": {longitude},\n' \
                  '"longitude_public": {longitude_public},\n' \
                  '"city": "{city}",\n' \
                  '"province": "{province}",\n' \
                  '"country": "{country}",\n' \
                  '"elevation": {elevation},\n' \
                  '"elevation_units": "{elevation_units}",\n' \
                  '"timestamp": "{timestamp}"\n' \
                  '}}'.format(value=record_data['value'],
                              value_units=record_data['value_units'],
                              value_error_range=record_data['value_error_range'],
                              timestamp=str(record_data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')),
                              latitude=record_data['latitude'],
                              latitude_public=float(int(record_data['latitude'] * 1000)) / 1000,
                              longitude=record_data['longitude'],
                              longitude_public=float(int(record_data['longitude'] * 1000)) / 1000,
                              city=record_data['city'],
                              province=record_data['province'],
                              country=record_data['country'],
                              elevation=record_data['elevation'],
                              elevation_units=record_data['elevation_units'])

        log.debug('payload= {payload}'.format(payload=payload))

        headers = {
            'content-type': 'application/json',
            'cache-control': 'no-cache'
        }

        response = requests.request('PUT', app_url, data=payload, headers=headers)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=401)
        )

        assert response.status_code == 401, 'Expected a HTTP status code 401'

        log.info('End')

    def test_step_07_update_record_with_auth(self):
        """Update a temperature record with JWT token."""
        log = logging.getLogger("TestCase.test_step_07_update_record_with_auth")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/{last_id}'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource,
            last_id=TestCaseProtectedTemperature.last_id
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('app_url= {url}'.format(url=app_url))

        record_data = get_random_record_data()

        payload = '{{\n' \
                  '"value": {value},\n' \
                  '"value_units": "{value_units}",\n' \
                  '"value_error_range": {value_error_range},\n' \
                  '"latitude": {latitude},\n' \
                  '"latitude_public": {latitude_public},\n' \
                  '"longitude": {longitude},\n' \
                  '"longitude_public": {longitude_public},\n' \
                  '"city": "{city}",\n' \
                  '"province": "{province}",\n' \
                  '"country": "{country}",\n' \
                  '"elevation": {elevation},\n' \
                  '"elevation_units": "{elevation_units}",\n' \
                  '"timestamp": "{timestamp}"\n' \
                  '}}'.format(value=record_data['value'],
                              value_units=record_data['value_units'],
                              value_error_range=record_data['value_error_range'],
                              timestamp=str(record_data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')),
                              latitude=record_data['latitude'],
                              latitude_public=float(int(record_data['latitude'] * 1000)) / 1000,
                              longitude=record_data['longitude'],
                              longitude_public=float(int(record_data['longitude'] * 1000)) / 1000,
                              city=record_data['city'],
                              province=record_data['province'],
                              country=record_data['country'],
                              elevation=record_data['elevation'],
                              elevation_units=record_data['elevation_units'])

        log.debug('payload= {payload}'.format(payload=payload))

        headers = {
            'content-type': 'application/json',
            'authorization': 'JWT {token}'.format(token=TestCaseProtectedTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('PUT', app_url, data=payload, headers=headers)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=204)
        )

        assert response.status_code == 204, 'Expected a HTTP status code 204'
        self.assertEqual(len(response.text), 0), 'Expected data in the response'

        log.info('End')

    def test_step_08_get_all_records_without_auth(self):
        """Get all temperature records without JWT token."""
        log = logging.getLogger("TestCase.test_step_08_get_all_records_without_auth")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('app_url= {url}'.format(url=app_url))

        headers = {
            'cache-control': 'no-cache'
        }

        querystring = {"start": "0001-01-01", "end": "9999-12-31"}

        response = requests.request('GET', app_url, headers=headers, data='', params=querystring)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=401)
        )

        assert response.status_code == 401, 'Expected a HTTP status code 401'

        json_data = json.loads(response.text)

        for item in json_data:
            log.debug(str(item))

        log.info('End')

    def test_step_09_get_all_records_with_auth(self):
        """Get all temperature records with JWT token."""
        log = logging.getLogger("TestCase.test_step_09_get_all_records_with_auth")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('app_url= {url}'.format(url=app_url))

        headers = {
            'authorization': 'JWT {token}'.format(token=TestCaseProtectedTemperature.token),
            'cache-control': 'no-cache'
        }

        querystring = {"start": "0001-01-01", "end": "9999-12-31"}

        response = requests.request('GET', app_url, headers=headers, data='', params=querystring)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=200)
        )

        assert response.status_code == 200, 'Expected a HTTP status code 200'

        json_data = json.loads(response.text)

        for item in json_data:
            log.debug(str(item))

        log.info('End')

    def test_step_10_delete_record_without_auth(self):
        """Delete a temperature record without JWT token."""
        log = logging.getLogger("TestCase.test_step_10_delete_record_without_auth")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/{last_id}'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource,
            last_id=TestCaseProtectedTemperature.last_id
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('app_url= {url}'.format(url=app_url))

        payload = ''

        log.debug('payload= {payload}'.format(payload=payload))

        headers = {
            'cache-control': 'no-cache'
        }

        response = requests.request('DELETE', app_url, data=payload, headers=headers)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=401)
        )

        assert response.status_code == 401, 'Expected a HTTP status code 401'

        log.info('End')

    def test_step_11_delete_record_with_auth(self):
        """Delete a temperature record with JWT token."""
        log = logging.getLogger("TestCase.test_step_11_delete_record_with_auth")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/{last_id}'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource,
            last_id=TestCaseProtectedTemperature.last_id
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('app_url= {url}'.format(url=app_url))

        payload = ''

        log.debug('payload= {payload}'.format(payload=payload))

        headers = {
            'authorization': 'JWT {token}'.format(token=TestCaseProtectedTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('DELETE', app_url, data=payload, headers=headers)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=204)
        )

        assert response.status_code == 204, 'Expected a HTTP status code 204'
        self.assertEqual(len(response.text), 0), 'Expected data in the response'

        log.info('End')

    def test_step_12_get_deleted_record_with_auth(self):
        """Get a deleted temperature record with JWT token."""
        log = logging.getLogger("TestCase.test_step_12_get_deleted_record_with_auth")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/{last_id}'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource,
            last_id=TestCaseProtectedTemperature.last_id
        )

        log.debug('base_url= {url}'.format(url=self.base_url))
        log.debug('app_url= {url}'.format(url=app_url))

        headers = {
            'authorization': 'JWT {token}'.format(token=TestCaseProtectedTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('GET', app_url, headers=headers)

        log.debug('Got {response_code} - expected {expected_code}'.format(
            response_code=response.status_code,
            expected_code=404)
        )

        assert response.status_code == 404, 'Expected a HTTP status code 404'
        log.info('End')


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger('TestCase.test_step_00_login_fail').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_01_login').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_02_create_record_without_auth').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_03_create_record_with_auth').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_03_1_create_record_with_auth_out_of_range_latitude').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_03_2_create_record_with_auth_out_of_range_latitude').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_03_3_create_record_with_auth_out_of_range_longitude').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_03_4_create_record_with_auth_out_of_range_longitude').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_04_get_record_without_auth').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_05_get_record_with_auth').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_06_update_record_without_auth').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_07_update_record_with_auth').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_08_get_all_records_without_auth').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_09_get_all_records_with_auth').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_10_delete_record_without_auth').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_11_delete_record_with_auth').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_12_get_deleted_record_with_auth').setLevel(logging.DEBUG)
    unittest.main()
