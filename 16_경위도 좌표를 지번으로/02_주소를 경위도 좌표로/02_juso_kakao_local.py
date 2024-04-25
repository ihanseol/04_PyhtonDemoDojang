"""
using kakao local api
date : 2024/4/26


"""

import requests

# api 정보 셋팅
url = "https://dapi.kakao.com/v2/local/search/address.json"
REST_API_KEY = "***"
headers = {"Authorization": "KakaoAK {}".format(REST_API_KEY)}

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

addr = str(srchwrd)
print('address : ', addr)

params = {"query": f"{addr}"}  # 주소정보를 파라미터에  담습니다.
print('url:', url)
print('params:', params)
print('headers:', headers)

resp = requests.get(url, params=params, headers=headers)  # 해더와 파라미터 정보를 넣어 get 타입으로 전송합니다.

documents = resp.json()["documents"]  # json으로 받은 파일을 파싱하기.
print('documents : ', documents)

address = ""
road_address = ""

if len(documents) > 0:  # json을 파싱후 documents 에 데이터가 있을 경우에만
    address = documents[0]['address']['address_name']  # 지번주소
    road_address = documents[0]['road_address']['address_name']  # 도로명 주소

print(address)
print(road_address)
