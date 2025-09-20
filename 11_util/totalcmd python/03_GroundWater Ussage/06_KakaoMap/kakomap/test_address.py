"""
using kakao local api
date : 2025/3/14
"""
import json
import requests
import pyperclip

# api 정보 셋팅
url = "https://dapi.kakao.com/v2/local/search/address.json"
REST_API_KEY = "bb159a41d2eb8d5acb71e0ef1dde4d16"
# headers = {"Authorization": "KakaoAK {}".format(REST_API_KEY)}
headers = {"Authorization": f"KakaoAK {REST_API_KEY}"}


def extract_coordinates(data):
    if not data:
        return None, None

    first_item = data[0]  # 첫 번째 항목 사용

    x = first_item.get('x')
    y = first_item.get('y')

    return x, y


def transform_coordinates(x, y):
    url_b = f"https://dapi.kakao.com/v2/local/geo/transcoord.json?x={x}&y={y}&input_coord=WGS84&output_coord=TM"
    response = requests.get(url_b, headers=headers)
    url_text = json.loads(response.text)
    x = url_text['documents'][0]['x']
    y = url_text['documents'][0]['y']

    print(f"x: {x}")
    print(f"y: {y}")
    print("-" * 100)

    pyperclip.copy(f"{x},{y}")
    print(f"{x},{y}")


def test_address():
    addr = "충청남도 예산군 대술면 화산리 607-1"
    params = {"query": f"{addr}"}  # 주소정보를 파라미터에  담습니다.

    resp = requests.get(url, params=params, headers=headers)  # 해더와 파라미터 정보를 넣어 get 타입으로 전송합니다.
    documents = resp.json()["documents"]  # json으로 받은 파일을 파싱하기.

    print("-" * 100)
    print('documents : ', documents)

    address_data = ""
    road_address = ""

    if len(documents) > 0:  # json을 파싱후 documents 에 데이터가 있을 경우에만
        address_data = documents[0]['address']['address_name']  # 지번주소
        # road_address = documents[0]['road_address']['address_name']  # 도로명 주소

    print("-" * 100)
    print(address_data)
    # print(road_address)
    print("-" * 100)
    # 함수 실행
    x, y = extract_coordinates(documents)
    print(f"x: {x}, y: {y}")

    print("-" * 100)
    transform_coordinates(x, y)
    print("-" * 100)

    input('종료하시려면 엔터키를 누르세요 ~ ')


if __name__ == '__main__':
    test_address()
