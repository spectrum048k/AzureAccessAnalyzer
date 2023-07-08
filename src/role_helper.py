import json


# function to create a role based on a list of actions
def create_role(actions):
    with open("sample_role.json", "r") as read_file:
        role = json.load(read_file)

        role["properties"]["permissions"][0]["actions"] = actions
        return role
