import http
import json
import uuid
import requests
from loguru import logger
from azure.identity import DefaultAzureCredential


class AzureAPI:
    """Wrapper for the Azure REST API"""

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
        try:
            uuid.UUID(guid)
            return True
        except Exception:
            return False

    def get_default_azure_credential(self):
        """Use DefaultAzureCredential to authenticate"""
        credential = DefaultAzureCredential()

        # get the access token
        gettoken = credential.get_token("https://management.azure.com/.default")

        return gettoken.token

    def get_token_header(self):
        """Gets an access token using the client credentials flow"""

        # use the default azure credential to login and get an access token
        access_token = self.get_default_azure_credential()

        return {"Authorization": f"Bearer {access_token}"}

    def check_response(self, response):
        """Check the response status code and return the json body if successful"""

        if response.status_code == http.HTTPStatus.OK:
            return response.json()
        else:
            raise SystemError(f"Response error: {response.text}")

    def http_get(self, url):
        """HTTP GET request"""
        response = requests.get(url, headers=self.get_token_header())

        self.log_response_info(response)

        return response

    def log_response_info(self, response):
        """log the response return code, headers and body"""

        logger.debug(f"Response status code: {response.status_code}")

        for header, value in response.headers.items():
            logger.debug(f"Response ('header:', '{header}:', '{value}')")

        logger.debug(f"Response body: {response.text}")
