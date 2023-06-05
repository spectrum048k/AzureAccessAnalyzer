import sys
import traceback
from azure_activity_logs import AzureActivityLogs
from azure_management import AzureManagement
from azure_roles import AzureRoles
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

def check_actions_used():
    """ return the actions used by the user in the last n hours"""

    sub_id, user_name, num_hours, rg_name = validate_arguments()

    start_date, end_date = datetime_helper.get_last_n_hours(num_hours)
    select = None

    az = AzureActivityLogs()
    activity_log = az.get_activity_log(sub_id, start_date, end_date, rg_name, select, user_name)

    # extract the operation values
    operations = [x['operationName']['value'] for x in activity_log['value']]

    # sort and remove duplicates
    operations = sorted(list(set(operations)))

    logger.info(f'List of operations for {user_name} between {start_date} and {end_date}:')
    logger.info(az.format_json_object(operations))

    if operations and len(operations) > 0:
        role = role_helper.create_role(operations)
        logger.info('Sample role based on actions:')
        logger.info(az.format_json_object(role))

def check_role_assignments():
    sub_id = sys.argv[1]

    az = AzureRoles()

    # list the role assignments for the subscription
    role_assignments = az.get_role_assignments(sub_id)

    properties = [x['properties'] for x in role_assignments['value']]

    # extract the role assignment principalId and principalType from role_assignments
    result = [{'principalId': x['principalId'], 
                        'principalType': x['principalType'],
                        'scope': x['scope'],
                        'roleDefinitionId': x['roleDefinitionId']} for x in properties]
                
    logger.info(f"{len(result)} role assignments for subscription {sub_id}:")
    logger.info(az.format_json_object(result))

def check_subs_and_rgs():
    """ Check the subscriptions and resource groups for the tenant"""

    az = AzureManagement()

    # list the subscriptions for the tenant
    subscriptions = az.get_subscriptions()
    logger.info(f"subscriptions: {az.format_json_object(subscriptions)}")
    
    for sub in subscriptions['value']:
        sub_id = sub['subscriptionId']
        resource_groups = az.get_resource_groups(sub_id)

        # get the name, location and tags (if they exist) for each resource group
        resource_groups = [{'name': x['name'], 'location': x['location'], 'tags': x['tags'] if 'tags' in x else None} for x in resource_groups['value']]
        
        logger.info(f"resource groups for subscription {sub_id}: {az.format_json_object(resource_groups)}")

def main():
    try:
        logger.info("Starting up...")

        # check if the user has used any actions in the last n hours
        check_actions_used()

        # check the role assignments for the subscription
        # check_role_assignments()

        # check subs and resource groups
        # check_subs_and_rgs()
    except Exception as e:
        logger.error(f"Unexpected exception occurred: {e}")
        logger.error(f"Stack trace: {traceback.print_exc()}")
        sys.exit(1)

# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    main()
