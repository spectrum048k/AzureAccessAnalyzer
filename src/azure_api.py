import datetime
import http
import requests
from loguru import logger

class AzureAPI():
    """ Wrapper for the Azure REST API"""
    # Note: Azure REST API is used as the Azure Python SDK is not well documented and is inconsistent
    AZURE_REST_API_BASE_URL = "https://management.azure.com"

    def log_requests(self, *args):
        logger.debug(f"Request: {args}")

    def __init__(self, auth_headers):
        self.auth_headers = auth_headers
        http.client.HTTPConnection.debuglevel = 1
        http.client.print = self.log_requests
    
    def get_subscriptions(self):
        """ Get the list of subscriptions """
        url = f"{self.AZURE_REST_API_BASE_URL}/subscriptions?api-version=2021-01-01"
        response = requests.get(url, headers=self.auth_headers)
        return response.json()['value']
    
    def get_resource_groups(self, subscription_id):
        """ Get the list of resource groups """
        # validate subscription_id is a valid GUID
        self.is_valid_guid(subscription_id)

        # build the url using base url, subscription_id and api version
        url = f"{self.AZURE_REST_API_BASE_URL}/subscriptions/{subscription_id}/resourcegroups?api-version=2020-06-01"
        response = requests.get(url, headers=self.auth_headers)
        return response.json()
    
    def get_activity_log(self, subscription_id:str, start_date:datetime, end_date:datetime,
                         resource_group=None, select=None, userName=None):
        """ Get the activity log for a subscription between two dates"""

        # validate subscription_id is a valid GUID
        self.is_valid_guid(subscription_id)
        
        # validate start_date is before end_date
        if start_date > end_date:
            raise Exception('start_date must be before end_date')
        
        # convert the dates to utc and to iso format
        start_date = start_date.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        end_date = end_date.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")

        filter = f"$filter=eventTimestamp ge '{start_date}' and eventTimestamp le '{end_date}'"

        if resource_group:
            filter += f" and resourceGroupName eq '{resource_group}'"

        if userName:
            filter += f" and caller eq '{userName}'"

        if select:
            filter += f"&$select={select}"

        url = f"{self.AZURE_REST_API_BASE_URL}/subscriptions/{subscription_id}/providers/microsoft.insights/eventtypes/management/values?api-version=2017-03-01-preview&{filter}&{select}"

        response = requests.get(url, headers=self.auth_headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error getting activity log: {response.text}")

    def is_valid_guid(self, guid):
        if not guid or not isinstance(guid, str) or not len(guid) == 36:
            raise Exception('value must be a valid GUID')