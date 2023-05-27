import http
import json
import os
import requests
from loguru import logger

class AzureAPI():
    """ Wrapper for the Azure REST API"""
    # Note: Azure REST API is used as the Azure Python SDK is not well documented and is inconsistent
    AZURE_REST_API_BASE_URL = "https://management.azure.com"

    def log_requests(self, *args):
        logger.debug(f"Request {args}")

    def __init__(self):
        http.client.HTTPConnection.debuglevel = 1
        http.client.HTTPSConnection.debuglevel = 1
        http.client.print = self.log_requests
    
    def format_json_object(self, obj):
        return json.dumps(obj, indent=4)

    def is_valid_guid(self, guid):
        if not guid or not isinstance(guid, str) or len(guid) != 36:
            raise ValueError('value must be a valid GUID')
        
    def get_token_header(self):
        """Gets an access token using the client credentials flow"""

        tenant_id = os.environ.get("TENANT_ID")
        client_id = os.environ.get("CLIENT_ID")
        client_secret = os.environ.get("CLIENT_SECRET")

        # check variables are set
        if not tenant_id and not AzureAPI.is_valid_guid(tenant_id):
            raise ValueError('TENANT_ID environment variable is not set or invalid.')
        if not client_id and not AzureAPI.is_valid_guid(client_id):
            raise ValueError('CLIENT_ID environment variable is not set or invalid.')
        if not client_secret:
            raise ValueError('CLIENT_SECRET environment variable is not set.')

        # Get an access token using the client credentials flow
        url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials',
            'scope': 'https://management.azure.com/.default'
        }

        response = requests.post(url, data=data)

        self.log_response_info(response)

        access_token = response.json()['access_token']

        return {'Authorization': f'Bearer {access_token}'}

    def check_response(self, response):
        """ Check the response status code and return the json body if successful"""

        if response.status_code == http.HTTPStatus.OK:
            return response.json()
        else:
            raise SystemError(f"Response error: {response.text}")

    def http_get(self, url):
        """ HTTP GET request """
        response = requests.get(url, headers=self.get_token_header())

        self.log_response_info(response)

        return response

    def log_response_info(self, response):
        """ log the response return code, headers and body """

        logger.debug(f"Response status code: {response.status_code}")

        for header, value in response.headers.items():
            logger.debug(f"Response ('header:', '{header}:', '{value}')")

        logger.debug(f"Response body: {response.text}")
    

    

