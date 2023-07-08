from azure_api import AzureAPI


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
