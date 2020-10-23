import geoip2.database
import maxminddb


def geo_db_path(type):
    return f'/var/lib/GeoIP/GeoLite2-{type}.mmdb'


def geoip_info(ip_address):
    """Retrieves Geolocation information for a given IP address
    using the MaxMinds GeoIP2 Lite Database

    Args:
        ip_address (String): The IP Address to be looked up in database

    Returns:
        [Dict]: The resulting geolocation information for the given IP,
        including coordintes, ASN information, etc...
    """
    try:
        result = dict()

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
            print(response)

        return result
    except (FileNotFoundError, maxminddb.InvalidDatabaseError) as e:
        # TODO: Add log here
        raise e
    except (geoip2.errors.AddressNotFoundError):
        # TODO: Add address not found log here
        pass
    except (ValueError):
        # TODO: Add bad IP log here
        pass
