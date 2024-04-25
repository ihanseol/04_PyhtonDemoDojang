import json

# Your JSON data
json_data = [
    {
        "address": {
            "address_name": "대전 유성구 장대동 278-13",
            "b_code": "3020011700",
            "h_code": "3020054000",
            "main_address_no": "278",
            "mountain_yn": "N",
            "region_1depth_name": "대전",
            "region_2depth_name": "유성구",
            "region_3depth_h_name": "온천2동",
            "region_3depth_name": "장대동",
            "sub_address_no": "13",
            "x": "127.334896600034",
            "y": "36.3590896879659"
        },
        "address_name": "대전 유성구 장대동 278-13",
        "address_type": "REGION_ADDR",
        "road_address": {
            "address_name": "대전 유성구 유성대로740번길 26",
            "building_name": "",
            "main_building_no": "26",
            "region_1depth_name": "대전",
            "region_2depth_name": "유성구",
            "region_3depth_name": "장대동",
            "road_name": "유성대로740번길",
            "sub_building_no": "",
            "underground_yn": "N",
            "x": "127.334926308569",
            "y": "36.3591064566676",
            "zone_no": "34172"
        },
        "x": "127.334896600034",
        "y": "36.3590896879659"
    }
]

# Parse JSON


str_data = json.dumps(json_data, ensure_ascii=False)
data = json.loads(str_data)

# Extract zone_no
zone_no = data[0]['road_address']['zone_no']

# Extract x, y
x = data[0]['address']['x']
y = data[0]['address']['y']

print("Zone No:", zone_no)
print("X coordinate:", x)
print("Y coordinate:", y)
print(f"{y},{x}")


