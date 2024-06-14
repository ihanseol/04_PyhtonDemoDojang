import pandas as pd
import requests 
import sys
import json
import datetime 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#I referred github of HanewSuh for this program (https://github.com/henewsuh).
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def json_request(url='', encoding='utf-8', success=None, error=lambda e: print('%s : %s' % (e, datetime.now()), file=sys.stderr)):
    headers = {'Authorization': 'KakaoAK {}'.format(APP_KEY)}
    resp = requests.get(url, headers=headers)
    # print('%s : success for request [%s]' % (datetime.now(), url))
    return resp.text

def reverse_geocode(longitude, latitude):
    # 파라미터 최적화하여 url 생성
    url = '%s?x=%s&y=%s' %(URL, longitude, latitude)
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
 
def get_address(x,y):
    address = []        
    json_name, json_code = reverse_geocode(x, y) 
    address.append(json_name)
    return address # 전처리 함수에서 주소 리스트 받아서 데이터프레임에 추가

def get_code(x,y):
    code = []        
    json_name, json_code = reverse_geocode(x, y) 
    code.append(json_code)
    return code # 전처리 함수에서 행정구역코드 리스트 받아서 데이터프레임에 추가
    

#RESET API KEY
APP_KEY = 'dd647f9b693ff95ef2eb636d34df3be3' 
URL = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json'

#READ
df_all = pd.read_csv('long_lat_fault.csv')

#LABEL
df_all.columns = ['long','lat']

#ADD THE COLUME OF ADDRESS
df_all["address"] = ""

df_all
 
df = df_all[['long', 'lat','address']]

for i in range(len(df)): 
    x_crd = float(df.loc[i, ['long']])
    y_crd = float(df.loc[i, ['lat']])
   
#    print(x_crd,y_crd)
    address = get_address(x_crd, y_crd)
#    print(address)
#    code = get_code(x_crd, y_crd)

#    print(code)

    df.loc[i, ['address']] = address
#    df.loc[i, ['CODE']] = code
    
   
print(df.info)   
    
    
    
