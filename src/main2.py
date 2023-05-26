import os
import sys
import traceback
import azure_api
from loguru import logger

def main():  # sourcery skip: extract-method
    try:
        logger.info("Starting up...")
        
        azure = azure_api.AzureAPI(auth_headers)

        sub_id = sys.argv[1]

        # list the role assignments for the subscription
        role_assignments = azure.get_role_assignments(sub_id)

        properties = [x['properties'] for x in role_assignments['value']]

        # extract the role assignment principalId and principalType from role_assignments
        result = [{'principalId': x['principalId'], 
                            'principalType': x['principalType'],
                            'scope': x['scope'],
                            'roleDefinitionId': x['roleDefinitionId']} for x in properties]
                   
        logger.info(f"{len(result)} role assignments for subscription {sub_id}:")
        logger.info(azure_api.AzureAPI.format_json_object(result))
    except Exception as e:
        logger.error(f'Exception: {e}')
        logger.error(traceback.format_exc())
        sys.exit(1)

# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    main()