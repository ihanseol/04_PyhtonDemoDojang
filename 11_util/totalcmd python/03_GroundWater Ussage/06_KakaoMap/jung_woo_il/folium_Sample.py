import pandas as pd
import numpy as np
import pyproj
import folium

df = pd.read_csv(r"d:\05_Send\fulldata_07_24_04_P_일반음식점.csv",
                 encoding='cp949',
                 usecols=['좌표정보x(epsg5174)','좌표정보y(epsg5174)'])

print(df.head())
print(len(df))

print(df)



df = df.dropna()
df.index=range(len(df))
print(df.tail())


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


def project_array_modern(coord, p1_type, p2_type):
    """
    좌표계 변환 함수 (Coordinate Transformation Function)
    - coord: x, y 좌표 정보가 담긴 NumPy Array
    - p1_type: 입력 좌표계 정보 ex) "epsg:5179"
    - p2_type: 출력 좌표계 정보 ex) "epsg:4326"
    """

    # 1. Address FutureWarning: '+init=<authority>:<code>' syntax is deprecated
    #    Use pyproj.Transformer.from_crs, passing the EPSG strings directly.
    #    This avoids initializing pyproj.Proj manually.
    transformer = pyproj.Transformer.from_crs(
        p1_type,
        p2_type,
        # always_xy=True ensures the input/output order is always (longitude, latitude)
        # or (easting, northing) which is usually (x, y).
        # This helps manage axis order changes.
        always_xy=True
    )

    # 2. Address FutureWarning: This function is deprecated (pyproj.transform)
    #    Use the modern transformer.transform() method instead.
    fx, fy = transformer.transform(coord[:, 0], coord[:, 1])

    return np.dstack([fx, fy])[0]


coord = np.array(df)
print(coord)

p1_type = "epsg:5174"
p2_type = "epsg:4326"

result = project_array_modern(coord, p1_type, p2_type)
print(result)

# df['경도'] = result[:, 0]
# df['위도'] = result[:, 1]
df.loc[:, '경도'] = result[:, 0] # Assign E-W coordinate (경도)
df.loc[:, '위도'] = result[:, 1] # Assign N-S coordinate (위도)
print(df.tail())

# 데이터 100개 랜덤 추출
sample = df.sample(n=100)

# 지도 중심 좌표 설정
lat_c, lon_c = 37.53165351203043, 126.9974246490573

# Folium 지도 객체 생성
m = folium.Map(location=[lat_c, lon_c], zoom_start=6)

# 마커 생성
for _, row in sample.iterrows():
    lat, lon = row['위도'], row['경도']
    folium.Marker(location=[lat, lon]).add_to(m)

print(m)

# ⭐️ Folium 맵 객체를 HTML 파일로 저장
m.save("map_of_restaurants.html")










