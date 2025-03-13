import json
from datetime import datetime
import sys
import pandas as pd
import requests


def json_request(url='', encoding='utf-8', success=None,
                 error=lambda e: print('%s : %s' % (e, datetime.now()), file=sys.stderr)):
    headers = {'Authorization': 'KakaoAK {}'.format(APP_KEY)}
    resp = requests.get(url, headers=headers)
    # print('%s : success for request [%s]' % (datetime.now(), url))
    return resp.text


def reverse_geocode(longitude, latitude):
    # 파라미터 최적화하여 url 생성
    url = '%s?x=%s&y=%s' % (URL, longitude, latitude)
    # json request
    try:
        # print('try')
        json_req = json_request(url=url)
        json_data = json.loads(json_req)
        json_doc = json_data.get('documents')[0]
        json_name = json_doc.get('address_name')
        json_code = json_doc.get('code')
    except:
        # print('nan')
        json_name = 'NaN'
        json_code = 'NaN'
    return json_name, json_code


def get_address(x, y):
    address = []
    json_name, json_code = reverse_geocode(x, y)
    address.append(json_name)
    return address  # 전처리 함수에서 주소 리스트 받아서 데이터프레임에 추가


def get_code(x, y):
    code = []
    json_name, json_code = reverse_geocode(x, y)
    code.append(json_code)
    return code  # 전처리 함수에서 행정구역코드 리스트 받아서 데이터프레임에 추가


APP_KEY = 'here'
URL = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json'

df_all = pd.read_csv('서울시_병의원_위치_정보.csv', encoding='cp949')
df = df_all[['기관ID', '병원경도', '병원위도']]  # 기관ID, 병원경도, 병원위도 열만 추출 (도로명주소는 일부러 날림)

print(df)


for i in range(len(df)):
    x_crd = float(df.loc[i, ['병원경도']])
    y_crd = float(df.loc[i, ['병원위도']])
    address = get_address(x_crd, y_crd)
    code = get_code(x_crd, y_crd)
    df.loc[i, ['ADDRESS']] = address
    df.loc[i, ['CODE']] = code

    if i % 100 == 0:
        print('{} 번째 경위도 좌표계에 대한 정보 불러오는 중...'.format(i))
