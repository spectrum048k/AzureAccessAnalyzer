import sys
import traceback
from azure_activity_logs import AzureActivityLogs
import azure_api
import datetime_helper
import role_helper
from loguru import logger

def validate_arguments():
    # Get the command-line arguments
    args = sys.argv
    logger.debug(f'Command-line arguments: {args}')

    if len(args) < 3:
        raise ValueError('Subscription ID and user name are required arguments')

    sub_id = args[1]
    user_name = args[2]

    # check if there is a third argument num hours which should be a positive integer
    if len(args) > 3:
        try:
            num_hours = int(args[3])
            if num_hours < 1:
                raise ValueError('num_hours must be a positive integer')

        except ValueError as e:
            raise ValueError('num_hours must be a positive integer') from e
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

def check_permissions_used():
    sub_id, user_name, num_hours, rg_name = validate_arguments()

    start_date, end_date = datetime_helper.get_last_n_hours(num_hours)
    select = None

    az = AzureActivityLogs()
    activity_log = az.get_activity_log(sub_id, start_date, end_date, rg_name, select, user_name)

    # extract the operation values
    operations = [x['operationName']['value'] for x in activity_log['value']]

    logger.debug('List of operations:')
    logger.debug(azure_api.AzureAPI.format_json_object(operations))

    # sort and remove duplicates
    operations = sorted(list(set(operations)))

    logger.info(f'List of operations for {user_name} between {start_date} and {end_date}:')
    logger.info(azure_api.AzureAPI.format_json_object(operations))

    if operations and len(operations) > 0:
        role = role_helper.create_role(operations)
        logger.info('Sample role based on actions:')
        logger.info(azure_api.AzureAPI.format_json_object(role))

def main():
    try:
        logger.info("Starting up...")

        check_permissions_used()

    except Exception as e:
        logger.error(f"Unexpected exception occurred: {e}")
        logger.error(f"Stack trace: {traceback.print_exc()}")
    
# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    main()
