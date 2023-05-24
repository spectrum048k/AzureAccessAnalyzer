import sys
import traceback
import azure_api
import azure_api_helper
import os
import json
import datetime_helper
import role_helper
from loguru import logger

def format_object(obj):
    return json.dumps(obj, indent=4)

def validate_arguments():
    # Get the command-line arguments
    args = sys.argv
    logger.debug(f'Command-line arguments: {args}')

    if len(args) < 3:
        raise Exception('Subscription ID and user name are required arguments')
    
    sub_id = args[1]
    user_name = args[2]

    # check if there is a third argument num hours which should be a positive integer
    if len(args) > 3:
        try:
            num_hours = int(args[3])
            if num_hours < 1:
                raise ValueError('num_hours must be a positive integer')
            
        except ValueError:
            raise Exception('num_hours must be a positive integer')
    else:
        logger.debug('num_hours not specified, defaulting to 1')
        num_hours = 1

    # check fourth optional arument rg_name
    if len(args) > 4:
        rg_name = args[4]
    else:
        logger.debug('rg_name not specified, defaulting to None')
        rg_name = None

    return sub_id, user_name, num_hours, rg_name

def main():
    try:
        logger.info("Starting up...")

        sub_id, user_name, num_hours, rg_name = validate_arguments()

        auth_headers = azure_api_helper.get_token_header(
            os.environ.get("TENANT_ID"), 
            os.environ.get("CLIENT_ID"), 
            os.environ.get("CLIENT_SECRET"))

        azure = azure_api.AzureAPI(auth_headers)

        start_date, end_date = datetime_helper.get_last_n_hours(num_hours)
        select = None

        activity_log = azure.get_activity_log(sub_id, start_date, end_date, rg_name, select, user_name)

        # extract the operation values
        operations = [x['operationName']['value'] for x in activity_log['value']]

        logger.debug(f'List of operations:')
        logger.debug(format_object(operations))

        # sort and remove duplicates
        operations = sorted(list(set(operations)))

        logger.info(f'List of operations for {user_name} between {start_date} and {end_date}:')
        logger.info(format_object(operations))

        if operations and len(operations) > 0:
            role = role_helper.create_role(operations)
            logger.info('Sample role based on actions:')
            logger.info(format_object(role))
            
    except Exception as e:
        logger.error(f"Unexpected exception occurred: {e}")
        logger.error(f"Stack trace: {traceback.print_exc()}")
    
# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    main()
