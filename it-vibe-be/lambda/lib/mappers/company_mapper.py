def map(company_object):
    try:
        company_vo = {
            "id": company_object["id"],
            "name": company_object["name"],
            "description": company_object["description"],
            "location": company_object["location"],
            "creationDate": company_object["creationDate"],
            "updateDate": company_object["updateDate"],
            "siren": company_object["siren"],
            "siret": company_object["siret"],
            "president": company_object["president"],
            "adress": company_object["adress"],
            "country": company_object["country"],
            "size": company_object["size"],
            "revenue": company_object["revenue"],
            "industry": company_object["industry"],
            "IBAN": company_object["IBAN"],

        }
        return company_vo
    except KeyError as e:
        # Handle missing keys in company_object
        print(f"KeyError: {e}")
        return None
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")
        return None