import json
import requests

def format_object(obj):
    return json.dumps(obj, indent=4)

def get_token_header(tenant_id, client_id, client_secret):
    """Gets an access token using the client credentials flow"""

    # check variables are set
    if not tenant_id:
        raise ValueError('TENANT_ID environment variable is not set.')
    if not client_id:
        raise ValueError('CLIENT_ID environment variable is not set.')
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