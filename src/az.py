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
    
    def get_resource_groups(self):
        """ Get the list of reource groups """
        url = "https://management.azure.com/subscriptions/0b1f6471-1bf0-4dda-aec3-cb9272f09590/resourcegroups?api-version=2020-06-01"
        response = requests.get(url, headers=self.auth_headers)
        return response.json()