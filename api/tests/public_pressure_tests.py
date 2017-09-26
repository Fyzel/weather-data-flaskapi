"""
@author:     Fyzel@users.noreply.github.com

@copyright:  2017 Englesh.org. All rights reserved.

@license:    https://github.com/Fyzel/weather-data-flaskapi/blob/master/LICENSE

@contact:    Fyzel@users.noreply.github.com
@deffield    updated: 2017-06-14
"""

import json
import logging
import sys
import unittest
from json import loads
import requests

class TestCasePublicPressure(unittest.TestCase):
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
        self.resource = 'PublicPressureData'

    def tearDown(self):
        pass

    def test_step_00_get_all_records_without_auth(self):
        """Get all records without JWT token."""
        log = logging.getLogger("TestCase.test_step_00_get_all_records_without_auth")
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
            expected_code=200)
        )

        assert response.status_code == 200, 'Expected a HTTP status code 401'

        json_data = json.loads(response.text)

        TestCasePublicPressure.last_id = None

        if len(json_data) > 0:
            TestCasePublicPressure.last_id = json_data[0]['id']

        log.info('End')

    def test_step_01_get_record_without_auth(self):
        """Get a public record without JWT token."""
        log = logging.getLogger("TestCase.test_step_01_get_record_without_auth")
        log.info('Start')

        if TestCasePublicPressure.last_id is not None:
            app_url = '{base_url}/{context}/{resource}/{last_id}'.format(
                base_url=self.base_url,
                context=self.context,
                resource=self.resource,
                last_id=TestCasePublicPressure.last_id
            )

            log.debug('base_url= {url}'.format(url=self.base_url))
            log.debug('app_url= {url}'.format(url=app_url))

            headers = {
                'cache-control': 'no-cache'
            }

            response = requests.request('GET', app_url, headers=headers)

            log.debug('Got {response_code} - expected {expected_code}'.format(
                response_code=response.status_code,
                expected_code=200)
            )

            assert response.status_code == 200, 'Expected a HTTP status code 401'

        log.info('End')


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger('TestCase.test_step_00_get_all_records_without_auth').setLevel(logging.DEBUG)
    logging.getLogger('TestCase.test_step_01_get_record_without_auth').setLevel(logging.DEBUG)
    unittest.main()
