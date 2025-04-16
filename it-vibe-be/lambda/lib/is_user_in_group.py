import json


def is_user_in_group(event, group_name):
    """
    Checks if the user is in the specified Cognito group.

    Args:
        event (dict): The Lambda event object.
        group_name (str): The name of the Cognito group to check.

    Returns:
        bool: True if the user is in the specified group, False otherwise.
    """
    try:
        # Extract the Cognito claims from the requestContext
        claims = event['requestContext']['authorizer']['claims']
        groups = claims.get('cognito:groups', '')

        # Check if the user is in the specified group
        return group_name in groups
    except KeyError:
        # If claims or groups are missing, return False
        return False