import logging
import geoip2.database
from contextlib import suppress

logger = logging.getLogger('maxminds-geodata')


def geo_db_path(type):
    """
    Returns the full path of a specific GeoLite2 database

    Args:
        type (str): The type of database path to retrieve (ASN, City, Country)

    Raises:
        ValueError: An invalid database type has been provided

    Returns:
        str: The absolute path to the specified database.
    """
    if type not in ['ASN', 'City', 'Country']:
        raise ValueError(
            "Invalid GeoLite2 Database type provided.\n"
            "Type must be: 'ASN', 'City' or 'Country'"
        )
    else:
        return f'/usr/local/share/GeoIP/GeoLite2-{type}.mmdb'


def geoip_info(ip_address):
    """Retrieves Geolocation information for a given IP address
    using the MaxMinds GeoIP2 Lite Database

    Args:
        ip_address (str): The IP Address to be looked up in database

    Returns:
        [dict]: The resulting geolocation information for the given IP,
            including coordintes, ASN information, etc...
    """
    result = {}
    with suppress(ValueError, geoip2.errors.AddressNotFoundError):
        with geoip2.database.Reader(geo_db_path('City')) as reader:
            response = reader.city(ip_address)

            result["city"] = {
                "names": response.city.names,
            }
            result["country"] = {
                "names": response.country.names,
                "iso_code": response.country.iso_code,
            }
            result["continent"] = {
                "code": response.continent.code,
                "names": response.continent.names,
            }
            result["coordinates"] = {
                "lat": response.location.latitude,
                "lng": response.location.longitude,
            }

        with geoip2.database.Reader(geo_db_path('ASN')) as reader:
            response = reader.asn(ip_address)

            result["asn"] = {
                "number": response.autonomous_system_number,
                "organisation": response.autonomous_system_organization,
            }

    return result
