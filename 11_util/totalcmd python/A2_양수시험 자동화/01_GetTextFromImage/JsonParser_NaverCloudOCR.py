import json

# Given JSON data
json_data = '''
{
    "version": "V2",
    "requestId": "dcda1db5-7a19-41bb-8a77-dbb2e95a5050",
    "timestamp": 1617947318461,
    "images": [
        {
            "uid": "33894645ee8e4b8094fe309e6efd30a2",
            "name": "demo",
            "inferResult": "SUCCESS",
            "message": "SUCCESS",
            "validationResult": {
                "result": "NO_REQUESTED"
            },
            "fields": [
                {
                    "valueType": "ALL",
                    "boundingPoly": {
                        "vertices": [
                            {
                                "x": 14.0,
                                "y": 20.0
                            },
                            {
                                "x": 273.0,
                                "y": 20.0
                            },
                            {
                                "x": 273.0,
                                "y": 95.0
                            },
                            {
                                "x": 14.0,
                                "y": 95.0
                            }
                        ]
                    },
                    "inferText": "CLOVA",
                    "inferConfidence": 1.0,
                    "type": "NORMAL",
                    "lineBreak": false
                },
                {
                    "valueType": "ALL",
                    "boundingPoly": {
                        "vertices": [
                            {
                                "x": 286.0,
                                "y": 20.0
                            },
                            {
                                "x": 454.0,
                                "y": 20.0
                            },
                            {
                                "x": 454.0,
                                "y": 93.0
                            },
                            {
                                "x": 286.0,
                                "y": 93.0
                            }
                        ]
                    },
                    "inferText": "OCR",
                    "inferConfidence": 1.0,
                    "type": "NORMAL",
                    "lineBreak": true
                },
                {
                    "valueType": "ALL",
                    "boundingPoly": {
                        "vertices": [
                            {
                                "x": 55.0,
                                "y": 213.0
                            },
                            {
                                "x": 107.0,
                                "y": 213.0
                            },
                            {
                                "x": 107.0,
                                "y": 245.0
                            },
                            {
                                "x": 55.0,
                                "y": 245.0
                            }
                        ]
                    },
                    "inferText": "참고",
                    "inferConfidence": 1.0,
                    "type": "NORMAL",
                    "lineBreak": true
                },
                {
                    "valueType": "ALL",
                    "boundingPoly": {
                        "vertices": [
                            {
                                "x": 59.0,
                                "y": 357.0
                            },
                            {
                                "x": 146.0,
                                "y": 357.0
                            },
                            {
                                "x": 146.0,
                                "y": 395.0
                            },
                            {
                                "x": 59.0,
                                "y": 395.0
                            }
                        ]
                    },
                    "inferText": "네이버",
                    "inferConfidence": 1.0,
                    "type": "NORMAL",
                    "lineBreak": false
                },
                {
                    "valueType": "ALL",
                    "boundingPoly": {
                        "vertices": [
                            {
                                "x": 150.0,
                                "y": 359.0
                            },
                            {
                                "x": 267.0,
                                "y": 359.0
                            },
                            {
                                "x": 267.0,
                                "y": 395.0
                            },
                            {
                                "x": 150.0,
                                "y": 395.0
                            }
                        ]
                    },
                    "inferText": "클라우드",
                    "inferConfidence": 1.0,
                    "type": "NORMAL",
                    "lineBreak": false
                },
                {
                    "valueType": "ALL",
                    "boundingPoly": {
                        "vertices": [
                            {
                                "x": 269.0,
                                "y": 357.0
                            },
                            {
                                "x": 385.0,
                                "y": 357.0
                            },
                            {
                                "x": 385.0,
                                "y": 395.0
                            },
                            {
                                "x": 269.0,
                                "y": 395.0
                            }
                        ]
                    },
                    "inferText": "플랫폼의",
                    "inferConfidence": 0.9999,
                    "type": "NORMAL",
                    "lineBreak": false
                }
            ]
        }
    ]
}
'''

# Parse the JSON data
data = json.loads(json_data)

# Extract the "inferText" field from each field in the images array
infer_texts = [field['inferText'] for image in data['images'] for field in image['fields']]

# Print the extracted "inferText" values
for text in infer_texts:
    print(text)
