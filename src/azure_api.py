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
    
    @staticmethod
    def format_json_object(obj):
        return json.dumps(obj, indent=4)

    @staticmethod
    def is_valid_guid(guid):
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
        auth_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials',
            'scope': 'https://management.azure.com/.default'
        }

        response = requests.post(auth_url, data=data)
        access_token = response.json()['access_token']

        return {'Authorization': f'Bearer {access_token}'}

    def http_get(self, url):
        """ HTTP GET request """
        response = requests.get(url, headers=self.get_token_header())

        logger.debug(f"Response status code: {response.status_code}")

        for header, value in response.headers.items():
            logger.debug(f"Response ('header:', '{header}:', '{value}')")

        logger.debug(f"Response body: {response.text}")

        return response
    
    def get_subscriptions(self):
        """ Get the list of subscriptions """
        url = f"{self.AZURE_REST_API_BASE_URL}/subscriptions?api-version=2021-01-01"
        response = requests.get(url, headers=self.auth_headers)
        return response.json()['value']
    
    def get_resource_groups(self, subscription_id):
        # sourcery skip: class-extract-method
        """ Get the list of resource groups """
        self.is_valid_guid(subscription_id)

        # build the url using base url, subscription_id and api version
        url = f"{self.AZURE_REST_API_BASE_URL}/subscriptions/{subscription_id}/resourcegroups?api-version=2020-06-01"
        response = requests.get(url, headers=self.auth_headers)
        return response.json()
    
    # get role assignments for subscription
    def get_role_assignments(self, subscription_id):    
        """ Get the role assignments for a subscription """
        self.is_valid_guid(subscription_id)

        # build the url using base url, subscription_id and api version
        url = f"{self.AZURE_REST_API_BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Authorization/roleAssignments?api-version=2022-04-01&$filter=atScope()"
        response = requests.get(url, headers=self.auth_headers)
        return response.json()
