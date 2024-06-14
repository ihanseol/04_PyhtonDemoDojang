from geopy.geocoders import Nominatim


def geocoding(address):
    geolocoder = Nominatim(user_agent='South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}

    return crd


crd = geocoding("대전시 유성구 장대동 278-13")
print(crd['lat'])
print(crd['lng'])

crd = geocoding("대전광역시 유성구 유성대로740번길 26")
print(crd['lat'])
print(crd['lng'])
