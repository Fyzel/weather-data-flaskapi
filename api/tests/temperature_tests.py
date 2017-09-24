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
    # microsecond = random.randint(0, 999999)

    return datetime(year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute,
                    second=second,
                    # microsecond=microsecond,
                    tzinfo=pytz.UTC)


def get_random_record_data():
    """Generate a random temperature data record"""
    value = float('{:.4f}'.format(random.uniform(-40.0, 40.0)))
    value_units = 'C'
    value_error_range = float('{:.6f}'.format(random.uniform(0.0, 1.0)))
    timestamp = get_random_datetime()
    latitude = float('{:.6f}'.format(random.uniform(-90.0, 90.0)))
    longitude = float('{:.6f}'.format(random.uniform(-180.0, 180.0)))
    elevation = float('{:.4f}'.format(random.uniform(-90.0, 999.0)))
    elevation_units = 'm'

    return {
        'value': value,
        'value_units': value_units,
        'value_error_range': value_error_range,
        'latitude': latitude,
        'longitude': longitude,
        'elevation': elevation,
        'elevation_units': elevation_units,
        'timestamp': timestamp
    }


class TestCaseTemperature(unittest.TestCase):
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
        self.resource = 'temperatures'
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

        log.debug("base_url= %r", self.base_url)

        auth_url = '{base_url}/auth'.format(base_url=self.base_url)

        log.debug("auth_url= %r", auth_url)
        log.debug("username= %r", self.username[::-1])  # reversed username
        log.debug("password= %r", self.password[::-1])  # reversed password

        payload = '{{"username": "{username_value}","password": "{password_value}"}}'.format(
            username_value=self.username[::-1],
            password_value=self.password[::-1]
        )

        log.debug("payload= %r", payload)

        headers = {
            'content-type': 'application/json',
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', auth_url, data=payload, headers=headers)

        assert response.status_code == 401, 'Expected a HTTP status code 401'
        assert len(response.text) > 0, 'Expected data in the response'

        log.debug("response.text= %r", response.text)

        log.info('End')

    def test_step_01_login(self):
        """Test the login capability and setup for the next set of calls"""
        log = logging.getLogger("TestCase.test_step_01_login")
        log.info('Start')

        log.debug("base_url= %r", self.base_url)

        auth_url = '{base_url}/auth'.format(base_url=self.base_url)

        log.debug("auth_url= %r", auth_url)
        log.debug("username= %r", self.username)
        log.debug("password= %r", self.password)

        payload = '{{"username": "{username_value}","password": "{password_value}"}}'.format(
            username_value=self.username,
            password_value=self.password
        )

        log.debug("payload= %r", payload)

        headers = {
            'content-type': 'application/json',
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', auth_url, data=payload, headers=headers)

        assert response.status_code == 200, 'Expected a HTTP status code 200'
        assert len(response.text) > 0, 'Expected data in the response'

        log.debug("response.text= %r", response.text)

        json_data = json.loads(response.text)

        assert json_data['access_token'] is not None, 'Access token is not returned'

        TestCaseTemperature.token = json_data['access_token']

        log.debug("JWT token= %r", self.token)

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

        log.debug("app_url= %r", app_url)

        record_data = get_random_record_data()

        payload = '{{"value": {value}, ' \
                  '"value_units": "{value_units}", ' \
                  '"value_error_range": {value_error_range}, ' \
                  '"timestamp": "{timestamp}", ' \
                  '"elevation": {elevation}, ' \
                  '"elevation_units": "{elevation_units}", ' \
                  '"latitude": {latitude}, ' \
                  '"longitude": {longitude}}}'.format(value=record_data['value'],
                                                      value_units=record_data['value_units'],
                                                      value_error_range=record_data['value_error_range'],
                                                      timestamp=str(record_data['timestamp'].strftime(
                                                          '%Y-%m-%dT%H:%M:%S')),
                                                      latitude=record_data['latitude'],
                                                      longitude=record_data['longitude'],
                                                      elevation=record_data['elevation'],
                                                      elevation_units=record_data['elevation_units'])

        log.debug("payload= %r", payload)

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

        log.debug("app_url= %r", app_url)

        record_data = get_random_record_data()

        payload = '{{"value": {value}, ' \
                  '"value_units": "{value_units}", ' \
                  '"value_error_range": {value_error_range}, ' \
                  '"latitude": {latitude}, ' \
                  '"longitude": {longitude}, ' \
                  '"elevation": {elevation}, ' \
                  '"elevation_units": "{elevation_units}", ' \
                  '"timestamp": "{timestamp}"}}'.format(value=record_data['value'],
                                                        value_units=record_data['value_units'],
                                                        value_error_range=record_data['value_error_range'],
                                                        latitude=record_data['latitude'],
                                                        longitude=record_data['longitude'],
                                                        elevation=record_data['elevation'],
                                                        elevation_units=record_data['elevation_units'],
                                                        timestamp=str(record_data['timestamp'].strftime(
                                                            '%Y-%m-%dT%H:%M:%S')))

        log.debug("payload= %r", payload)

        headers = {
            'content-type': 'application/json',
            'authorization': 'JWT {token}'.format(token=TestCaseTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', app_url, data=payload, headers=headers)

        log.debug('status code: {status_code}'.format(status_code=response.status_code))

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
            json_data['longitude'],
            record_data['longitude']), 'Returned longitude is the same'

        TestCaseTemperature.last_id = json_data['id']
        TestCaseTemperature.previous_record = record_data

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

        log.debug("app_url= %r", app_url)

        record_data = get_random_record_data()

        payload = '{{"value": {value}, ' \
                  '"value_units": "{value_units}", ' \
                  '"value_error_range": {value_error_range}, ' \
                  '"latitude": {latitude}, ' \
                  '"longitude": {longitude}, ' \
                  '"elevation": {elevation}, ' \
                  '"elevation_units": "{elevation_units}", ' \
                  '"timestamp": "{timestamp}"}}'.format(value=record_data['value'],
                                                        value_units=record_data['value_units'],
                                                        value_error_range=record_data['value_error_range'],
                                                        latitude=-91.0,
                                                        longitude=record_data['longitude'],
                                                        elevation=record_data['elevation'],
                                                        elevation_units=record_data['elevation_units'],
                                                        timestamp=str(
                                                            record_data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')))

        log.debug("payload= %r", payload)

        headers = {
            'content-type': 'application/json',
            'authorization': 'JWT {token}'.format(token=TestCaseTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', app_url, data=payload, headers=headers)

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

        log.debug("app_url= %r", app_url)

        record_data = get_random_record_data()

        payload = '{{"value": {value}, ' \
                  '"value_units": "{value_units}", ' \
                  '"value_error_range": {value_error_range}, ' \
                  '"latitude": {latitude}, ' \
                  '"longitude": {longitude}, ' \
                  '"elevation": {elevation}, ' \
                  '"elevation_units": "{elevation_units}", ' \
                  '"timestamp": "{timestamp}"}}'.format(value=record_data['value'],
                                                        value_units=record_data['value_units'],
                                                        value_error_range=record_data['value_error_range'],
                                                        latitude=91.0,
                                                        longitude=record_data['longitude'],
                                                        elevation=record_data['elevation'],
                                                        elevation_units=record_data['elevation_units'],
                                                        timestamp=str(
                                                            record_data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')))

        log.debug("payload= %r", payload)

        headers = {
            'content-type': 'application/json',
            'authorization': 'JWT {token}'.format(token=TestCaseTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', app_url, data=payload, headers=headers)

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

        log.debug("app_url= %r", app_url)

        record_data = get_random_record_data()

        payload = '{{"value": {value}, ' \
                  '"value_units": "{value_units}", ' \
                  '"value_error_range": {value_error_range}, ' \
                  '"latitude": {latitude}, ' \
                  '"longitude": {longitude}, ' \
                  '"elevation": {elevation}, ' \
                  '"elevation_units": "{elevation_units}", ' \
                  '"timestamp": "{timestamp}"}}'.format(value=record_data['value'],
                                                        value_units=record_data['value_units'],
                                                        value_error_range=record_data['value_error_range'],
                                                        latitude=record_data['latitude'],
                                                        longitude=-181.0,
                                                        elevation=record_data['elevation'],
                                                        elevation_units=record_data['elevation_units'],
                                                        timestamp=str(
                                                            record_data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')))

        log.debug("payload= %r", payload)

        headers = {
            'content-type': 'application/json',
            'authorization': 'JWT {token}'.format(token=TestCaseTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', app_url, data=payload, headers=headers)

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

        log.debug("app_url= %r", app_url)

        record_data = get_random_record_data()

        payload = '{{"value": {value}, ' \
                  '"value_units": "{value_units}", ' \
                  '"value_error_range": {value_error_range}, ' \
                  '"latitude": {latitude}, ' \
                  '"longitude": {longitude}, ' \
                  '"elevation": {elevation}, ' \
                  '"elevation_units": "{elevation_units}", ' \
                  '"timestamp": "{timestamp}"}}'.format(value=record_data['value'],
                                                        value_units=record_data['value_units'],
                                                        value_error_range=record_data['value_error_range'],
                                                        latitude=record_data['latitude'],
                                                        longitude=181.0,
                                                        elevation=record_data['elevation'],
                                                        elevation_units=record_data['elevation_units'],
                                                        timestamp=str(
                                                            record_data['timestamp'].strftime('%Y-%m-%dT%H:%M:%S')))

        log.debug("payload= %r", payload)

        headers = {
            'content-type': 'application/json',
            'authorization': 'JWT {token}'.format(token=TestCaseTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('POST', app_url, data=payload, headers=headers)

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
            last_id=TestCaseTemperature.last_id
        )

        log.debug("app_url= %r", app_url)

        headers = {
            'cache-control': 'no-cache'
        }

        response = requests.request('GET', app_url, headers=headers)

        assert response.status_code == 200, 'Expected a HTTP status code 200'

        json_data = json.loads(response.text)

        self.assertEqual(
            int(json_data['id']),
            int(TestCaseTemperature.last_id)), "Returned id is the same"
        self.assertEqual(
            json_data['value'],
            TestCaseTemperature.previous_record['value']), 'Returned value is the same'
        self.assertEqual(
            json_data['value_units'],
            TestCaseTemperature.previous_record['value_units']), 'Returned value_units is the same'
        self.assertEqual(
            json_data['value_error_range'],
            TestCaseTemperature.previous_record['value_error_range']), 'Returned value_error_range is the same'
        self.assertEqual(
            json_data['timestamp'],
            str(TestCaseTemperature.previous_record['timestamp'].strftime(
                '%Y-%m-%dT%H:%M:%S'))), 'Returned timestamp is the same'
        self.assertEqual(
            json_data['elevation'],
            TestCaseTemperature.previous_record['elevation']), 'Returned elevation is the same'
        self.assertEqual(
            json_data['elevation_units'],
            TestCaseTemperature.previous_record['elevation_units']), 'Returned elevation_units is the same'
        self.assertEqual(
            json_data['latitude'],
            TestCaseTemperature.previous_record['latitude']), 'Returned latitude is the same'
        self.assertEqual(
            json_data['longitude'],
            TestCaseTemperature.previous_record['longitude']), 'Returned longitude is the same'

        log.info('End')

    def test_step_05_get_record_with_auth(self):
        """Get a temperature record with JWT token."""
        log = logging.getLogger("TestCase.test_step_05_get_record_with_auth")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/{last_id}'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource,
            last_id=TestCaseTemperature.last_id
        )

        log.debug("app_url= %r", app_url)

        headers = {
            'authorization': 'JWT {token}'.format(token=TestCaseTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('GET', app_url, headers=headers)

        assert response.status_code == 200, 'Expected a HTTP status code 200'

        json_data = json.loads(response.text)

        self.assertEqual(
            int(json_data['id']),
            int(TestCaseTemperature.last_id)), "Returned id is the same"
        self.assertEqual(
            json_data['value'],
            TestCaseTemperature.previous_record['value']), 'Returned value is the same'
        self.assertEqual(
            json_data['value_units'],
            TestCaseTemperature.previous_record['value_units']), 'Returned value_units is the same'
        self.assertEqual(
            json_data['value_error_range'],
            TestCaseTemperature.previous_record['value_error_range']), 'Returned value_error_range is the same'
        self.assertEqual(
            json_data['timestamp'],
            str(TestCaseTemperature.previous_record['timestamp'].strftime(
                '%Y-%m-%dT%H:%M:%S'))), 'Returned timestamp is the same'
        self.assertEqual(
            json_data['elevation'],
            TestCaseTemperature.previous_record['elevation']), 'Returned elevation is the same'
        self.assertEqual(
            json_data['elevation_units'],
            TestCaseTemperature.previous_record['elevation_units']), 'Returned elevation_units is the same'
        self.assertEqual(
            json_data['latitude'],
            TestCaseTemperature.previous_record['latitude']), 'Returned latitude is the same'
        self.assertEqual(
            json_data['longitude'],
            TestCaseTemperature.previous_record['longitude']), 'Returned longitude is the same'

        log.info('End')

    def test_step_06_update_record_without_auth(self):
        """Update a temperature record without JWT token."""
        log = logging.getLogger("TestCase.test_step_06_update_record_without_auth")
        log.info('Start')

        app_url = '{base_url}/{context}/{resource}/{last_id}'.format(
            base_url=self.base_url,
            context=self.context,
            resource=self.resource,
            last_id=TestCaseTemperature.last_id
        )

        log.debug("app_url= %r", app_url)

        record_data = get_random_record_data()

        payload = '{{"value": {value}, ' \
                  '"value_units": "{value_units}", ' \
                  '"value_error_range": {value_error_range}, ' \
                  '"timestamp": "{timestamp}", ' \
                  '"elevation": {elevation}, ' \
                  '"elevation_units": "{elevation_units}", ' \
                  '"latitude": {latitude}, ' \
                  '"longitude": {longitude}}}'.format(value=record_data['value'],
                                                      value_units=record_data['value_units'],
                                                      value_error_range=record_data['value_error_range'],
                                                      timestamp=str(record_data['timestamp'].strftime(
                                                          '%Y-%m-%dT%H:%M:%S')),
                                                      elevation=record_data['elevation'],
                                                      elevation_units=record_data['elevation_units'],
                                                      latitude=record_data['latitude'],
                                                      longitude=record_data['longitude'])

        log.debug("payload= %r", payload)

        headers = {
            'content-type': 'application/json',
            'cache-control': 'no-cache'
        }

        response = requests.request('PUT', app_url, data=payload, headers=headers)

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
            last_id=TestCaseTemperature.last_id
        )

        log.debug("app_url= %r", app_url)

        record_data = get_random_record_data()

        payload = '{{"value": {value}, ' \
                  '"value_units": "{value_units}", ' \
                  '"value_error_range": {value_error_range}, ' \
                  '"timestamp": "{timestamp}", ' \
                  '"elevation": {elevation}, ' \
                  '"elevation_units": "{elevation_units}", ' \
                  '"latitude": {latitude}, ' \
                  '"longitude": {longitude}}}'.format(value=record_data['value'],
                                                      value_units=record_data['value_units'],
                                                      value_error_range=record_data['value_error_range'],
                                                      timestamp=str(record_data['timestamp'].strftime(
                                                          '%Y-%m-%dT%H:%M:%S')),
                                                      elevation=record_data['elevation'],
                                                      elevation_units=record_data['elevation_units'],
                                                      latitude=record_data['latitude'],
                                                      longitude=record_data['longitude'])

        log.debug("payload= %r", payload)

        headers = {
            'content-type': 'application/json',
            'authorization': 'JWT {token}'.format(token=TestCaseTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('PUT', app_url, data=payload, headers=headers)

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

        log.debug("app_url= %r", app_url)

        headers = {
            'cache-control': 'no-cache'
        }

        querystring = {"start": "0001-01-01", "end": "9999-12-31"}

        response = requests.request('GET', app_url, headers=headers, data='', params=querystring)

        assert response.status_code == 200, 'Expected a HTTP status code 200'

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

        log.debug("app_url= %r", app_url)

        headers = {
            'authorization': 'JWT {token}'.format(token=TestCaseTemperature.token),
            'cache-control': 'no-cache'
        }

        querystring = {"start": "0001-01-01", "end": "9999-12-31"}

        response = requests.request('GET', app_url, headers=headers, data='', params=querystring)

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
            last_id=TestCaseTemperature.last_id
        )

        log.debug("app_url= %r", app_url)

        payload = ''

        log.debug("payload= %r", payload)

        headers = {
            'cache-control': 'no-cache'
        }

        response = requests.request('DELETE', app_url, data=payload, headers=headers)

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
            last_id=TestCaseTemperature.last_id
        )

        log.debug("app_url= %r", app_url)

        payload = ''

        log.debug("payload= %r", payload)

        headers = {
            'authorization': 'JWT {token}'.format(token=TestCaseTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('DELETE', app_url, data=payload, headers=headers)

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
            last_id=TestCaseTemperature.last_id
        )

        log.debug("app_url= %r", app_url)

        headers = {
            'authorization': 'JWT {token}'.format(token=TestCaseTemperature.token),
            'cache-control': 'no-cache'
        }

        response = requests.request('GET', app_url, headers=headers)

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
