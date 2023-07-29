from azure.azure_api import AzureAPI


class AzureRoles(AzureAPI):
    """Class to manage Azure roles"""

    def __init__(self):
        super().__init__()

        # get role assignments for subscription

    def get_role_assignments(self, subscription_id):
        """Get the role assignments for a subscription"""

        self.is_valid_guid(subscription_id)

        # build the url using base url, subscription_id and api version
        url = f"{super().AZURE_REST_API_BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Authorization/roleAssignments?api-version=2022-04-01&$filter=atScope()"

        response = super().http_get(url)

        return super().check_response(response)

    def get_role_assignments_for_user(self, user_id, management_group_id):
        """Get the role assignments for a user"""

        # build the url using base url, subscription_id and api version
        url = f"{super().AZURE_REST_API_BASE_URL}/providers/Microsoft.Management/managementGroups/{management_group_id}/providers/Microsoft.Authorization/roleAssignments?api-version=2021-04-01-preview&$filter=assignedTo('{user_id}')"

        response = super().http_get(url)

        return super().check_response(response)
    
    def get_role_assignments_for_user_subscription(self, user_id, subscription_id):
        """Get the role assignments for a user"""

        # build the url using base url, subscription_id and api version
        url = f"{super().AZURE_REST_API_BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Authorization/roleAssignments?api-version=2022-04-01&$filter=principalId eq '{user_id}'"

        response = super().http_get(url)

        return super().check_response(response)

    def get_role_definitions(self):
        """ lists all role definitions in Azure tenant"""

        # build the url using base url, subscription_id and api version
        url = f"{super().AZURE_REST_API_BASE_URL}/providers/Microsoft.Authorization/roleDefinitions?api-version=2022-04-01"

        response = super().http_get(url)

        return super().check_response(response)
    
    def get_role_definition(self, role_definition_id):
        """ get the role definition for the given role definition id"""

        # build the url using base url, subscription_id and api version
        url = f"{super().AZURE_REST_API_BASE_URL}/{role_definition_id}?api-version=2022-04-01"

        response = super().http_get(url)

        return super().check_response(response)