import geoip2.database
import maxminddb
# import json


def geoip_info(ip_address):
    """Retrieves Geolocation information for a given IP address using the MaxMinds GeoIP2 Lite Database

    Args:
        ip_address (String): The IP Address to be looked up in database

    Returns:
        [Dict]: The resulting geolocation information for the given IP, 
        including coordintes, ASN information, etc...
    """
    try:
        result = dict()

        with geoip2.database.Reader('/var/lib/GeoIP/GeoLite2-City.mmdb') as reader:
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
            
        with geoip2.database.Reader('/var/lib/GeoIP/GeoLite2-ASN.mmdb') as reader:
            response = reader.asn(ip_address)
            result["asn"] = {
                "number": response.autonomous_system_number,
                "organisation": response.autonomous_system_organization,

            }
            print(response)

        return result
    except (FileNotFoundError, maxminddb.InvalidDatabaseError) as e:
        # TODO: Add log here
        raise
    except (geoip2.errors.AddressNotFoundError):
        # TODO: Add address not found log here
        pass
    except (ValueError):
        # TODO: Add bad IP log here
        pass

# print(json.dumps(geoip_info('82.24.38.130'), indent=2))
