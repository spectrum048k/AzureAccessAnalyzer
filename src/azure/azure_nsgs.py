from azure.azure_api import AzureAPI


class AzureNSG(AzureAPI):
    """Class to manage NSGs"""

    def __init__(self):
        super().__init__()

    def get_nsgs(self, subscription_id, resource_group_name):
        """Get the list of NSGs for a resource group"""

        self.is_valid_guid(subscription_id)
        # self.is_valid_resource_group_name(resource_group_name)

        # build the url using base url, subscription_id and api version
        url = f"{super().AZURE_REST_API_BASE_URL}/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/networkSecurityGroups?api-version=2022-11-01"

        response = super().http_get(url)

        return super().check_response(response)

    def get_nsgs(self, subscription_id):
        """Get all the NSGs in a subscription"""

        self.is_valid_guid(subscription_id)

        # build the url using base url, subscription_id and api version
        url = f"{super().AZURE_REST_API_BASE_URL}/subscriptions/{subscription_id}/providers/Microsoft.Network/networkSecurityGroups?api-version=2022-11-01"

        response = super().http_get(url)

        return super().check_response(response)
