import json
import requests
import pprint
import logging

# Configure the logging settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='petstore.log'  # Specify the log file name
)

class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, url, request_type, data=None, expected_error=False):
        stop_flag = False
        while not stop_flag:
            if request_type == 'GET':
                response = requests.get(url)
            elif request_type == 'POST':
                response = requests.post(url, data=data)
            else:
                response = requests.delete(url)

            if not expected_error and response.status_code == 200:
                stop_flag = True
            elif expected_error:
                stop_flag = True

            # Log the request and response details
            logging.info(f'{request_type} example')
            logging.info(f'Request URL: {response.url}')
            logging.info(f'Status Code: {response.status_code}')
            logging.info(f'Reason: {response.reason}')
            logging.info(f'Response Text: {response.text}')

            try:
                # Attempt to parse the response as JSON
                response_json = response.json()
                logging.info(f'Response JSON: {response_json}')
            except json.JSONDecodeError as e:
                # Handle the case where the response is not valid JSON
                logging.warning(f'Error decoding response JSON: {str(e)}')
                response_json = None  # Set to None or handle accordingly

            logging.info('**********')

        return response, response_json

    def get(self, endpoint, endpoint_id, expected_error=False):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response, response_json = self._request(url, 'GET', expected_error=expected_error)
        return response_json

    def post(self, endpoint, endpoint_id, body):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'POST', data=body)
        return response.json()['message']

    def delete(self, endpoint, endpoint_id):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'DELETE')
        return response.json()['message']

# Base URL for the Petstore API
BASE_URL_PETSTORE = 'https://petstore.swagger.io/v2'
try:
    base_request = BaseRequest(BASE_URL_PETSTORE)
    logging.info('BaseRequest initialized successfully')
except Exception as e:
    logging.error(f'Exception occurred during initialization: {str(e)}')

# Get pet information with ID 1
pet_info = base_request.get('pet', 1)
pprint.pprint(pet_info)

# Create a new pet with data
data = {'name': 'Barsic'}
pet_id = base_request.post('pet', 1, data)

# Retrieve information about the newly created pet
pet_info = base_request.get('pet', pet_id)

# Assert that the name of the created pet matches the provided data
assert data['name'] == pet_info['name']

# Delete the pet
request_id = base_request.delete('pet', 1)

# Attempt to retrieve the deleted pet's information with an expected error
pet_info = base_request.get('pet', request_id, expected_error=True)
pprint.pprint(pet_info)
