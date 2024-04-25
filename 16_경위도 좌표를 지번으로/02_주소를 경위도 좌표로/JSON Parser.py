import json

# JSON data
json_data = '''
{
  "response": {
    "service": {
      "name": "address",
      "version": "2.0",
      "operation": "getcoord",
      "time": "30(ms)"
    },
    "status": "OK",
    "input": {
      "type": "road",
      "address": "유성대로740번길 26"
    },
    "refined": {
      "text": "대전광역시 유성구 유성대로740번길 26 (장대동)",
      "structure": {
        "level0": "대한민국",
        "level1": "대전광역시",
        "level2": "유성구",
        "level3": "장대동",
        "level4L": "유성대로740번길",
        "level4LC": "",
        "level4A": "온천2동",
        "level4AC": "3020054000",
        "level5": "26",
        "detail": ""
      }
    },
    "result": {
      "crs": "EPSG:4326",
      "point": {
        "x": "127.334926271",
        "y": "36.359098167"
      }
    }
  }
}
'''

# Parse JSON
data = json.loads(json_data)

# Extract x and y coordinates
x = float(data["response"]["result"]["point"]["x"])
y = float(data["response"]["result"]["point"]["y"])

print("X Coordinate:", x)
print("Y Coordinate:", y)
