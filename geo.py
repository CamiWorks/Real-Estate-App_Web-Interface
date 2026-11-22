# GEO-LOCATION API SET UP
from geopy.geocoders import Nominatim


# Geo localization change parameters from text to coordinates
def set_geolocation(address: str) -> tuple:
    # Initialize Nominatim geocoder
    geolocator = Nominatim(user_agent="geo_coder")

    # Geocode the address
    location = geolocator.geocode(address)

    if location:
        latitude = location.latitude
        longitude = location.longitude
        return str(float(latitude)), str(float(longitude))
    else:
        return ValueError('No able to process the request.')


# Set a determinated radious of an average 500 m
def set_geolocation_area(latitude, longitude) -> tuple:
    central_point = [float(latitude), float(longitude)]
    if central_point:
        # set for latitud in Canada the average in 0.001 for 1 km set average for 500 m per pin point
        radius = 0.005

        # Calculate the bounds
        min_latitude = central_point[0] - radius
        max_latitude = central_point[0] + radius
        min_longitude = central_point[1] - radius
        max_longitude = central_point[1] + radius

        return (
            str(max_latitude),
            str(min_latitude),
            str(max_longitude),
            str(min_longitude),
        )
    else:
        raise ValueError("No central point defined.")