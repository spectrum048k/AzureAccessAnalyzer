import datetime
from azure.azure_api import AzureAPI


class AzureActivityLogs(AzureAPI):
    """Class to get Azure Activity Logs"""

    def __init__(self):
        super().__init__()

    def get_activity_log(
        self,
        subscription_id: str,
        start_date: datetime,
        end_date: datetime,
        resource_group=None,
        select=None,
        userName=None,
    ):
        """Get the activity log for a subscription between two dates"""

        # validate subscription_id is a valid GUID
        super().is_valid_guid(subscription_id)

        # validate start_date is before end_date
        if start_date > end_date:
            raise ValueError("start_date must be before end_date")

        # convert the dates to utc and to iso format
        start_date = start_date.astimezone(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
        end_date = end_date.astimezone(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S"
        )

        filter_param = f"$filter=eventTimestamp ge '{start_date}' and eventTimestamp le '{end_date}'"

        if resource_group:
            filter_param += f" and resourceGroupName eq '{resource_group}'"

        if userName:
            filter_param += f" and caller eq '{userName}'"

        if select:
            filter_param += f"&$select={select}"

        url = f"{super().AZURE_REST_API_BASE_URL}/subscriptions/{subscription_id}/providers/microsoft.insights/eventtypes/management/values?api-version=2017-03-01-preview&{filter_param}&{select}"

        response = super().http_get(url)

        return super().check_response(response)
