import pandas as pd
import numpy as np
import pyproj
import folium


def project_array(coord, p1_type, p2_type):
    """
    좌표계 변환 함수
    - coord: x, y 좌표 정보가 담긴 NumPy Array
    - p1_type: 입력 좌표계 정보 ex) epsg:5179
    - p2_type: 출력 좌표계 정보 ex) epsg:4326
    """
    p1 = pyproj.Proj(init=p1_type)
    p2 = pyproj.Proj(init=p2_type)
    fx, fy = pyproj.transform(p1, p2, coord[:, 0], coord[:, 1])
    return np.dstack([fx, fy])[0]


df = pd.read_excel("c:/Users/minhwasoo/Downloads/data.xlsx")

df['좌표정보(x)'] = pd.to_numeric(df['좌표정보(x)'], errors="coerce")
df['좌표정보(y)'] = pd.to_numeric(df['좌표정보(y)'], errors="coerce")

df = df.dropna()
print(df)

df.index = range(len(df))
df.tail()
print(df.head())

# DataFrame -> NumPy Array 변환
coord = np.array(df)
print('cord', coord)


def run_follium():
    # 데이터 100개 랜덤 추출
    sample = df.sample(n=4)

    # 지도 중심 좌표 설정
    lat_c, lon_c = 37.53165351203043, 126.9974246490573

    # Folium 지도 객체 생성
    m = folium.Map(location=[lat_c, lon_c], zoom_start=6)

    # 마커 생성
    for _, row in sample.iterrows():
        lat, lon = row['위도'], row['경도']
        folium.Marker(location=[lat, lon]).add_to(m)

    m.save('map.html')



run_follium()

