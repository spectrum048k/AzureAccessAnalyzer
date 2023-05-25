import os
import sys
import traceback
import azure_api
import azure_api_helper
from loguru import logger

def main():  # sourcery skip: extract-method
    try:
        logger.info("Starting up...")

        auth_headers = azure_api_helper.get_token_header(
            os.environ.get("TENANT_ID"), 
            os.environ.get("CLIENT_ID"), 
            os.environ.get("CLIENT_SECRET"))
        
        azure = azure_api.AzureAPI(auth_headers)

        sub_id = sys.argv[1]

        # list the role assignments for the subscription
        role_assignments = azure.get_role_assignments(sub_id)

        properties = [x['properties'] for x in role_assignments['value']]

        # extract the role assignment principalId and principalType from role_assignments
        result = [{'principalId': x['principalId'], 
                            'principalType': x['principalType']} for x in properties]
                   
        logger.info(f"Role assignments in subscription {sub_id}:")
        logger.info(azure_api_helper.format_object(result))
    except Exception as e:
        logger.error(f'Exception: {e}')
        logger.error(traceback.format_exc())
        sys.exit(1)

# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    main()