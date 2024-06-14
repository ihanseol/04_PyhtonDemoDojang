"""

@ 2024/4/26일

이것은, VWORLD API 를 이용한, 주소 좌표 변환인데
일단 카카오에다 찍어보니, 잘 들어 맞는다.
적어도, 우리집의 경우에는 ...

"""

import requests
import json

apiurl = "https://api.vworld.kr/req/address?"
params = {
    "service": "address",
    "request": "getcoord",
    "crs": "epsg:4326",
    "address": "유성대로740번길 26",
    "format": "json",
    "type": "road",
    "key": "***"
}

response = requests.get(apiurl, params=params)

str_data = ""
if response.status_code == 200:
    json_data = response.json()
    # print(type(json_data))  # type <class 'dict'> 이다.
    str_data = json.dumps(json_data, ensure_ascii=False)
    print(json_data)

data = json.loads(str_data)

# Extract x and y coordinates
x = float(data["response"]["result"]["point"]["x"])
y = float(data["response"]["result"]["point"]["y"])

print("X Coordinate:", x)
print("Y Coordinate:", y)
