import json
import pytest
from index import lambda_handler

class TestLambdaFunction:
    def test_successful_update(self):
        event = {'httpMethod': 'POST','authorizationToken': 'allowme','body': json.dumps({'id': '1', 'Weather': 'Sunny'})}

        response = lambda_handler(event, None)
        assert response['statusCode'] == 200
        assert response['body'] == 'Successfully inserted data!'

    def test_missing_attributes(self):
        event = {'httpMethod': 'POST','authorizationToken': 'allowme','body': json.dumps({})}
        response = lambda_handler(event, None)
        assert response['statusCode'] == 400
        assert 'id" and "Weather" attributes are required' in response['body']

    def test_additional_attributes(self):
        event = {'httpMethod': 'POST','authorizationToken': 'allowme','body': json.dumps({'id': '1', 'Weather': 'Sunny', 'Temperature': '25°C'})}
        response = lambda_handler(event, None)
        assert response['statusCode'] == 400
        assert 'Only "id" and "Weather" attributes are allowed' in response['body']

    def test_invalid_json(self):
        event = {'httpMethod': 'POST','authorizationToken': 'allowme','body': 'Invalid JSON'}
        response = lambda_handler(event, None)
        assert response['statusCode'] == 400
        assert 'Request body is not valid JSON' in response['body']
