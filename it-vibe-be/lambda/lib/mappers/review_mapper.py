def map(review_object):
    try:
        review_vo = {
        "company_id": review_object["company_id"],
        "rating": review_object["rating"],
        "isAnonymous": review_object["isAnonymous"],
        "comment": review_object["comment"],
        "creationDate": review_object["creationDate"],
        "review_id": review_object["review_id"],
        # Map the owner object only if the review is not anonymous, and exclude user_id
        "owner": {
                "email": review_object["owner"]["email"],
                "username": review_object["owner"]["username"],
            } if not review_object["isAnonymous"] else None,
        }
        return review_vo
    except KeyError as e:
        # Handle missing keys in review_object
        print(f"KeyError: {e}")
        return None
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")
        return None