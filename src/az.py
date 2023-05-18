import datetime
import requests

def get_token_header(tenant_id, client_id, client_secret):
    # check variables are set
    if not tenant_id:
        raise Exception('TENANT_ID environment variable is not set.')
    if not client_id:
        raise Exception('CLIENT_ID environment variable is not set.')
    if not client_secret:
        raise Exception('CLIENT_SECRET environment variable is not set.')

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

    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    return headers

class AzureAPI():
    """ Wrapper for the Azure REST API"""
    """ The REST API is used as the python Azure SDK is not well documented"""

    def __init__(self, auth_headers):
        self.auth_headers = auth_headers
    
    def get_subscriptions(self):
        """ Get the list of subscriptions """
        url = "https://management.azure.com/subscriptions?api-version=2021-01-01"
        response = requests.get(url, headers=self.auth_headers)
        return response.json()['value']
    
    def get_resource_groups(self, subscription_id):
        """ Get the list of reource groups """
        # validate subscription_id is a valid GUID
        self.is_valid_guid(subscription_id)

        url = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups?api-version=2020-06-01"
        response = requests.get(url, headers=self.auth_headers)
        return response.json()
    
    # add an optional parameter to filter by resource group
    # add an optional parameter to select the fields to return
    # add an optional parameter to filter by the caller user name
    def get_activity_log(self, subscription_id:str, start_date:datetime, end_date:datetime,
                         resource_group=None, select=None, userName=None):
        
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

        url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/microsoft.insights/eventtypes/management/values?api-version=2017-03-01-preview&{filter}&{select}"
        response = requests.get(url, headers=self.auth_headers)
        return response.json()

    def is_valid_guid(self, guid):
        if not guid or not isinstance(guid, str) or not len(guid) == 36:
            raise Exception('value must be a valid GUID')