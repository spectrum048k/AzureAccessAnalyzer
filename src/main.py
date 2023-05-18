import az
import os
import json
import datetime_helper

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

    user_name = 'usera@eoghankennyoutlook.onmicrosoft.com'
    
    select = 'operationName'
    # select = None

    start_date, end_date = datetime_helper.get_last_hour()

    activity_log = azure.get_activity_log(sub_id, start_date, end_date, rg, select, user_name)

    print(f'activity log:\n{0}', format_object(activity_log))

# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    main()
