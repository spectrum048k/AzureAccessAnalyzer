import az
import os
import sys
import json
import datetime_helper
from loguru import logger

def format_object(obj):
    return json.dumps(obj, indent=4)

def main():
    # use json format for the logging to stdout and stderr
    # logger.remove()
    # logger.add(sys.stdout, format="{time} {level} {message}", level="DEBUG", serialize=True)
    logger.info("Starting up...")

    auth_headers = az.get_token_header(
        os.environ.get("TENANT_ID"), 
        os.environ.get("CLIENT_ID"), 
        os.environ.get("CLIENT_SECRET"))

    azure = az.AzureAPI(auth_headers)

    subs = azure.get_subscriptions()
    logger.debug(f'subscriptions:')
    logger.debug(format_object(subs))

    sub_id = subs[0]['subscriptionId']

    rg = 'rg-app-a-temp'
    user_name = 'usera@eoghankennyoutlook.onmicrosoft.com'
    start_date, end_date = datetime_helper.get_last_week()
    select = None

    activity_log = azure.get_activity_log(sub_id, start_date, end_date, rg, select, user_name)

    logger.debug(f'activity log response:')
    logger.debug(format_object(activity_log))

    # extract the operation values
    operations = [x['operationName']['value'] for x in activity_log['value']]

    logger.debug(f'List of operations:')
    logger.debug(format_object(operations))

    # sort and remove duplicates
    operations = sorted(list(set(operations)))

    logger.info(f'List of operations for {user_name} between {start_date} and {end_date}:')
    logger.info(format_object(operations))

# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    main()
