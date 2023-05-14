import az
import os
import json


auth_headers = az.get_token_header(
    os.environ.get("TENANT_ID"), 
    os.environ.get("CLIENT_ID"), 
    os.environ.get("CLIENT_SECRET"))

az = az.AzureAPI(auth_headers)

subs = json.dumps(az.get_subscriptions(), indent=4)

# print(type(subs))
print(subs)