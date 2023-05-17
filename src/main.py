import az
import os
import json

def format_object(obj):
    return json.dumps(obj, indent=4)

def main():
    auth_headers = az.get_token_header(
        os.environ.get("TENANT_ID"), 
        os.environ.get("CLIENT_ID"), 
        os.environ.get("CLIENT_SECRET"))

    azure = az.AzureAPI(auth_headers)

    subs = azure.get_subscriptions()
    print(f'subscriptions:\n{0}', format_object(subs))

    sub_id = subs[0]['subscriptionId']

    # rgs = azure.get_resource_groups(sub_id)
    # print(f'resource groups:\n{0}', format_object(rgs))
    rg = 'rg-app-a-temp'
    
    select = 'authorization,caller'
    select = 'authorization,operationName'
    # select = None
    activity_log = azure.get_activity_log(sub_id, '2023-05-01', '2023-05-10',rg, select)

    print(f'activity log:\n{0}', format_object(activity_log))

# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    main()
