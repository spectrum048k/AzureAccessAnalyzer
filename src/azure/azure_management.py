from azure.azure_api import AzureAPI


class AzureManagement(AzureAPI):
    """Class to manage Azure roles"""

    def __init__(self):
        super().__init__()

    def get_subscriptions(self):
        """Get the list of subscriptions"""

        url = f"{super().AZURE_REST_API_BASE_URL}/subscriptions?api-version=2021-01-01"

        response = super().http_get(url)

        return super().check_response(response)

    def get_subscription(self, management_group_id):
        """Get the list of subscriptions for the management group"""

        # GET https://management.azure.com/providers/Microsoft.Management/managementGroups/{groupId}/subscriptions?api-version=2020-05-01
        url = f"{super().AZURE_REST_API_BASE_URL}/providers/Microsoft.Management/managementGroups/{management_group_id}/subscriptions?api-version=2021-04-01"

        response = super().http_get(url)

        return super().check_response(response)

    def get_resource_groups(self, subscription_id):
        """Get the list of resource groups"""
        super().is_valid_guid(subscription_id)

        url = f"{super().AZURE_REST_API_BASE_URL}/subscriptions/{subscription_id}/resourcegroups?api-version=2020-06-01"

        response = super().http_get(url)

        return super().check_response(response)

    def get_management_group_entities(self, management_group_id):
        """Get the list of management group entities"""

        url = f"{super().AZURE_REST_API_BASE_URL}/providers/Microsoft.Management/managementGroups/{management_group_id}/descendants?api-version=2020-05-01"

        response = super().http_get(url)

        return super().check_response(response)
