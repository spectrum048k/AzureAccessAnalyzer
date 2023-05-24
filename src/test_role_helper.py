from role_helper import create_role


def test_create_role_with_actions():
    role = create_role(['Microsoft.Resources/subscriptions/resourceGroups/read', 
                 'Microsoft.Resources/subscriptions/resourceGroups/write', 
                 'Microsoft.Resources/subscriptions/resourceGroups/delete'])
    
    # check role contains the actions
    assert 'Microsoft.Resources/subscriptions/resourceGroups/read' in role['properties']['permissions'][0]['actions']
    