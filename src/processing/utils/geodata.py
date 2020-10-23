import geoip2.database
import maxminddb

def geoip_info(ip_address):
    try:
        with geoip2.database.Reader('/var/lib/GeoIP/GeoLite2-City.mmdb') as reader:
            response = reader.city(ip_address)
            return {
                "city": {
                    "names": response.city.names,
                },
                "country": {
                    "names": response.country.names,
                    "iso_code": response.country.iso_code,
                },
                "continent": {
                    "code": response.continent.code,
                    "names": response.continent.names,
                },
                "coordinates": {
                    "lat": response.location.latitude,
                    "lng": response.location.longitude,
                }
            }
    except (FileNotFoundError, maxminddb.InvalidDatabaseError) as e:
        # TODO: Add log here
        raise
    except (geoip2.errors.AddressNotFoundError):
        # TODO: Add address not found log here
        pass
    except (ValueError):
        # TODO: Add bad IP log here
        pass
