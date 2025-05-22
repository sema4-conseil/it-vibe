import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def map(company_object):
    try:
        company_vo = {
            "id": company_object["id"],
            "name": company_object["name"],
            "creationDate": company_object["creationDate"],
            "siren": company_object["siren"],
            "siret": company_object["siret"],
            "adress": company_object["adress"],
            "country": company_object["country"],
            "size": company_object["size"],
            "revenue": company_object["revenue"],
            "industry": company_object["industry"]
        }
        return company_vo
    except KeyError as e:
        logger.error(f"Map company: Missing mandatory field: {e}")
        raise ValueError(f"Internal error.")
    except Exception as e:
        logger.error(f"Map company:  Exception occured: {e}")
        raise Exception(f"Internal error.")