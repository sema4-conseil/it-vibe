def get_user_informations(event):
    """
        get user informations from cognito token
    """
    try:
        # Extract the Cognito claims from the requestContext
        claims = event['requestContext']['authorizer']['claims']
        user_id = claims.get('sub', '')
        email = claims.get('email', '')
        groups = claims.get('cognito:groups', '')
        username = claims.get('cognito:username', '')
        return user_id, email, groups, username
    except Exception as e:
        print(e)
        return None, None, None
