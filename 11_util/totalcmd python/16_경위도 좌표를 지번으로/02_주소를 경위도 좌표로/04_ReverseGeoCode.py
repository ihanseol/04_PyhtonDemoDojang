# 가입 없이 좌표->주소 변환
from geopy.geocoders import Nominatim


def geocoding_reverse(lat_lng_str):
    geolocoder = Nominatim(user_agent='South Korea', timeout=None)
    address = geolocoder.reverse(lat_lng_str)

    return address


address = geocoding_reverse('36.3588332, 127.3336925')
print(address)
