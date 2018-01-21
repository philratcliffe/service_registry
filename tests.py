import unittest
import requests
import json
import http_status


class TestServiceRegistry(unittest.TestCase):

    def test_add_service(self):
        data = {'service_name': 'test', 'service_version': '0.0.1'}
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}

        response = requests.post(
            'http://localhost:5000/services/v1.0',
            data=data_json,
            headers=headers)

        exptected_result = {
            "resp": {
                "service": "test",
                "version": "0.0.1",
                "change": "created",
            }
        }

        self.assertEqual(response.status_code, http_status.CREATED)
        self.assertEqual(response.json(), exptected_result)

    def test_invalid_add_service(self):
        data = {'srvc_nam': 'test', 'service_version': '0.0.1'}
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}

        response = requests.post(
            'http://localhost:5000/services/v1.0',
            data=data_json,
            headers=headers)

        self.assertEqual(response.status_code, http_status.BAD_REQUEST)


    def test_invalid_url(self):
        data = {'service_name': 'test', 'service_version': '0.0.1'}
        data_json = json.dumps(data)
        headers = {'Content-type': 'application/json'}

        response = requests.post(
            'http://localhost:5000/sevices/v1.0',
            data=data_json,
            headers=headers)

        self.assertEqual(response.status_code, http_status.NOT_FOUND)



if __name__ == "__main__":
    unittest.main()
