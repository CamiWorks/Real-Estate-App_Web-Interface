# GEO-LOCATION API SET UP
import requests


# Geo localization change parameters from text to coordinates
def set_geolocation(address: str) -> tuple:
    base_url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": address,
        "format": "json",
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200 and data:
        location = data[0]  # Take the first result
        latitude = float(location["lat"])
        longitude = float(location["lon"])
        return str(latitude), str(longitude)
    else:
        raise ConnectionRefusedError(f"Unable to Connect to {base_url}")


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
