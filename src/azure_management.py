from azure_api import AzureAPI

class AzureManagement(AzureAPI):
    """ Class to manage Azure roles"""

    def __init__(self):
      super().__init__()

    def get_subscriptions(self):
      """ Get the list of subscriptions """

      url = f"{super().AZURE_REST_API_BASE_URL}/subscriptions?api-version=2021-01-01"

      response = super().http_get(url)

      return super().check_response(response)
    
    def get_resource_groups(self, subscription_id):
        # sourcery skip: class-extract-method
        """ Get the list of resource groups """
        super().is_valid_guid(subscription_id)

        url = f"{super().AZURE_REST_API_BASE_URL}/subscriptions/{subscription_id}/resourcegroups?api-version=2020-06-01"

        response = super().http_get(url)

        return super().check_response(response)
    
