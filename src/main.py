import sys
import traceback
from azure.azure_activity_logs import AzureActivityLogs
from azure.azure_management import AzureManagement
from azure.azure_nsgs import AzureNSG
from azure.azure_roles import AzureRoles
import datetime_helper
from loguru import logger
import typer
import re

app = typer.Typer(
    name="AzureAccessAnalyzer",
    add_completion=False,
    help="IAM Access Analyzer for Azure",
)


@app.command()
def check_actions_used(
    subscription_id: str = typer.Argument(""),
    user_name: str = typer.Argument(""),
    num_hours: int = typer.Argument(1),
    rg_name: str = typer.Argument(None),
):
    """return the actions used by the user in the last n hours"""

    start_date, end_date = datetime_helper.get_last_n_hours(num_hours)
    select = None

    az = AzureActivityLogs()
    activity_log = az.get_activity_log(
        subscription_id, start_date, end_date, rg_name, select, user_name
    )

    # extract the operation values
    operations = [x["operationName"]["value"] for x in activity_log["value"]]

    # sort and remove duplicates
    operations = sorted(list(set(operations)))

    logger.info(
        f"List of operations for {user_name} between {start_date} and {end_date}:"
    )
    logger.info(az.format_json_object(operations))


@app.command()
def export_nsg_rules(
    management_group_id: str = typer.Argument(
        help="The id of the management group to export NSG rules for"
    ),
):
    """export the NSG rules for all resource groups under the management group"""

    az = AzureManagement()
    az_nsg = AzureNSG()

    # get each entity under the management group
    entities_list = az.get_management_group_entities(management_group_id)
    entities = entities_list["value"]

    # get the resource groups for each subscription
    for entity in entities:
        if entity["type"] != "Microsoft.Management/managementGroups":
            sub_id = entity["name"]
            sub_name = entity["properties"]["displayName"]
            sub_name_safe_file_name = re.sub(r'[\\/:*?"<>|]', "", sub_name)
            sub_name_safe_file_name = sub_name_safe_file_name.replace(" ", "-")

            nsgs = az_nsg.get_nsgs(sub_id)

            # print the number of NSGs
            logger.info(f"{len(nsgs['value'])} NSGs for subscription {sub_id}")
            logger.debug(az.format_json_object(nsgs["value"]))

            # loop through the NSGs and extract the rules
            for nsg in nsgs["value"]:
                logger.debug(az.format_json_object(nsg))

                # get the resource group name
                if match := re.search(
                    r"/subscriptions/.*/resourceGroups/([^/]+)", nsg["id"]
                ):
                    resource_group_name = match[1]
                    logger.debug(resource_group_name)
                else:
                    logger.error(
                        "Unable to extract resource group name from scope {az.format_json_object(nsg)}}"
                    )

                # extract the NSG rules
                nsg_security_rules = nsg["properties"]["securityRules"]
                logger.debug(az.format_json_object(nsg_security_rules))

                # extract the NSG name
                nsg_name = nsg["name"]

                # write the NSG rules to a file
                with open(
                    f"{sub_name_safe_file_name}-{resource_group_name}-{nsg_name}.json",
                    "w",
                ) as f:
                    f.write(az.format_json_object(nsg_security_rules))
        else:
            logger.info(f"Skipping child management group {entity['name']}")


def check_role_assignments():
    sub_id = sys.argv[1]

    az = AzureRoles()

    # list the role assignments for the subscription
    role_assignments = az.get_role_assignments(sub_id)

    properties = [x["properties"] for x in role_assignments["value"]]

    # extract the role assignment principalId and principalType from role_assignments
    result = [
        {
            "principalId": x["principalId"],
            "principalType": x["principalType"],
            "scope": x["scope"],
            "roleDefinitionId": x["roleDefinitionId"],
        }
        for x in properties
    ]

    logger.info(f"{len(result)} role assignments for subscription {sub_id}:")
    logger.info(az.format_json_object(result))


def check_subs_and_rgs(subscription_id: str, rg_name: str = None):
    """Check the subscriptions and resource groups for the tenant"""

    az = AzureManagement()

    # list the subscriptions for the tenant
    subscriptions = az.get_subscriptions()
    logger.info(f"subscriptions: {az.format_json_object(subscriptions)}")

    for sub in subscriptions["value"]:
        sub_id = sub["subscriptionId"]
        resource_groups = az.get_resource_groups(sub_id)

        # get the name, location and tags (if they exist) for each resource group
        resource_groups = [
            {
                "name": x["name"],
                "location": x["location"],
                "tags": x["tags"] if "tags" in x else None,
            }
            for x in resource_groups["value"]
        ]

        logger.info(
            f"resource groups for subscription {sub_id}: {az.format_json_object(resource_groups)}"
        )


def main():
    try:
        logger.info("Starting up...")

        app()
    except Exception as e:
        logger.error(f"Unexpected exception occurred: {e}")
        stacktrace = traceback.format_exc()
        logger.debug(f"Stack trace: {stacktrace}")
        sys.exit(1)


# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    main()
