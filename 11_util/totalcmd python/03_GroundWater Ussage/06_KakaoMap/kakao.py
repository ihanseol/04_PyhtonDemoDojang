"""
using kakao local api
date : 2025/3/14
"""
import json
import requests

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
    api_test = requests.get(url_b, headers=headers)
    url_text = json.loads(api_test.text)
    x = url_text['documents'][0]['x']
    y = url_text['documents'][0]['y']

    print(f"x: {x}")
    print(f"y: {y}")
    print("*"*80)
    print(f"{x},{y}")


def main():
    # addr = "대전시 유성구 장대동 278-13"

    print('=============== 도로명 주소 & 지번 주소 & 우편번호 =======================')
    print('1. 지번으로 검색\n2. 도로명으로 검색\n3. 우편번호\n')

    select = input('검색 방법 선택 : ')

    if select == '1':
        seach_se = 'dong'
        srchwrd = input('지번 입력(예: 주월동 408-1) : ')
    elif select == '2':
        seach_se = 'road'
        srchwrd = input('도로명 입력(예: 서문대로 745) : ')
    else:
        seach_se = 'post'
        srchwrd = input('우편번호 입력(예: 61725) : ')

    if not srchwrd:
        addr = "유성구 장대동 278-13"
    else:
        addr = str(srchwrd)

    print('address : ', addr)
    params = {"query": f"{addr}"}  # 주소정보를 파라미터에  담습니다.
    print('url:', url)
    print('params:', params)
    print('headers:', headers)

    resp = requests.get(url, params=params, headers=headers)  # 해더와 파라미터 정보를 넣어 get 타입으로 전송합니다.
    documents = resp.json()["documents"]  # json으로 받은 파일을 파싱하기.

    print('documents : ', documents)

    address_data = ""
    road_address = ""

    if len(documents) > 0:  # json을 파싱후 documents 에 데이터가 있을 경우에만
        address_data = documents[0]['address']['address_name']  # 지번주소
        road_address = documents[0]['road_address']['address_name']  # 도로명 주소

    print("-" * 100)
    print(address_data)
    print(road_address)
    print("-" * 100)
    # 함수 실행
    x, y = extract_coordinates(documents)
    print(f"x: {x}, y: {y}")

    print("-" * 100)
    transform_coordinates(x, y)
    print("-" * 100)

    input('종료하시려면 엔터키를 누르세요 ~ ')

if __name__ == '__main__':
    main()
