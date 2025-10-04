# 이것은, gropandas 는 파이썬 버전 3.11에서 돌려야 한다.
# pip install geopandas
# pip install shapely
#


import geopandas
from shapely.geometry import Point


def get_tm_cordinate(lon, lat, espgcode):
    """
    경위도 좌표(WGS84, EPSG:4326)를 입력받아
    지정된 TM 좌표계(espgcode)로 변환하고
    TM 좌표(x, y)를 반환하는 함수.

    Args:
        lon (float): 경도 (Longitude)
        lat (float): 위도 (Latitude)
        espgcode (str): 변환할 TM 좌표계의 EPSG 코드 (예: "EPSG:2097")

    Returns:
        tuple: 변환된 TM 좌표 (x, y)
    """
    # 1. Shapely Point 객체 생성
    point = Point(lon, lat)

    # 2. GeoSeries 객체 생성 (WGS84, EPSG:4326으로 정의)
    # GeoPandas는 기본적으로 WGS84(EPSG:4326)를 경위도의 표준으로 사용합니다.
    gdf = geopandas.GeoSeries([point], crs="EPSG:4326")

    # 3. to_crs() 메서드를 사용하여 지정된 EPSG 코드로 좌표 변환
    gdf_tm = gdf.to_crs(espgcode)

    # 4. 변환된 좌표(Point 객체)에서 TM 좌표 (x, y) 추출
    tm_x = gdf_tm.geometry.x.iloc[0]
    tm_y = gdf_tm.geometry.y.iloc[0]

    return tm_x, tm_y



def test1():
    # 1. 서울특별시청 좌표 (경위도, WGS84)
    seoul_lon = 126.9784  # 경도
    seoul_lat = 37.5668  # 위도

    # 2. 변환할 TM 좌표계 코드 (중부원점)
    tm_espg = "EPSG:2097"

    # 3. 함수 실행
    tm_x, tm_y = get_tm_cordinate(seoul_lon, seoul_lat, tm_espg)

    # 4. 결과 출력
    print("="*80)
    print(f"변환 전 경위도 (WGS84, EPSG:4326): ({seoul_lon}, {seoul_lat})")
    print(f"변환 후 TM 좌표 ({tm_espg}): ({tm_x:.2f}, {tm_y:.2f})")
    print(f"\nTM 좌표 변환이 완료되었습니다. (참고: TM 좌표는 미터(m) 단위입니다.)")
    print("=" * 80)
    print("\n\n\n")



def get_espg_transform(lon, lat, espg_src, espg_tgt):
    """
    특정 ESPG 좌표계(espg_src)의 좌표를 입력받아
    다른 ESPG 좌표계(espg_tgt)로 변환하고
    변환된 좌표(x, y)를 반환하는 함수.

    Args:
        lon (float): 출발지 좌표계에서의 X 또는 경도(Longitude)
        lat (float): 출발지 좌표계에서의 Y 또는 위도(Latitude)
        espg_src (str): 출발지 좌표계의 EPSG 코드 (예: "EPSG:4326")
        espg_tgt (str): 목적지 좌표계의 EPSG 코드 (예: "EPSG:2097")

    Returns:
        tuple: 변환된 목적지 좌표 (x_tgt, y_tgt)
    """
    # 1. Shapely Point 객체 생성
    point = Point(lon, lat)

    # 2. GeoSeries 객체 생성 및 출발지 CRS(좌표계) 정의
    # GeoSeries에 입력된 좌표(lon, lat)와 해당 좌표의 CRS(espg_src)를 지정합니다.
    gdf_src = geopandas.GeoSeries([point], crs=espg_src)

    # 3. to_crs() 메서드를 사용하여 목적지 EPSG 코드로 좌표 변환
    gdf_tgt = gdf_src.to_crs(espg_tgt)

    # 4. 변환된 좌표(Point 객체)에서 목적지 좌표 (x, y) 추출
    x_tgt = gdf_tgt.geometry.x.iloc[0]
    y_tgt = gdf_tgt.geometry.y.iloc[0]

    return x_tgt, y_tgt



def test2():
    # 1. 서울특별시청 좌표 (경위도, WGS84)
    src_x = 126.9784  # 경도
    src_y = 37.5668  # 위도

    # 2. 출발지 및 목적지 ESPG 코드 정의
    espg_src = "EPSG:4326"  # 출발지: WGS84 경위도
    espg_tgt = "EPSG:2097"  # 목적지: 중부원점 TM

    # 3. 함수 실행
    tgt_x, tgt_y = get_espg_transform(src_x, src_y, espg_src, espg_tgt)

    # 4. 결과 출력
    print("=" * 80)
    print(f"출발지 좌표 ({espg_src}): (X={src_x}, Y={src_y})")
    print(f"목적지 좌표 ({espg_tgt}): (X={tgt_x:.2f}, Y={tgt_y:.2f})")
    print("=" * 80)
    print("\n\n\n")




def test3():
    # 1. 서울시청의 중부원점 TM 좌표 (EPSG:2097)
    tm_x = 197825.96  # TM X
    tm_y = 449626.54  # TM Y

    # 2. 출발지 및 목적지 ESPG 코드 정의 (역변환)
    espg_src_rev = "EPSG:2097"  # 출발지: 중부원점 TM
    espg_tgt_rev = "EPSG:4326"  # 목적지: WGS84 경위도

    # 3. 함수 실행
    lon_rev, lat_rev = get_espg_transform(tm_x, tm_y, espg_src_rev, espg_tgt_rev)

    # 4. 결과 출력
    print("=" * 80)
    print(f"출발지 좌표 ({espg_src_rev}): (X={tm_x:.2f}, Y={tm_y:.2f})")
    print(f"목적지 좌표 ({espg_tgt_rev}): (경도={lon_rev:.4f}, 위도={lat_rev:.4f})")
    print("=" * 80)
    print("\n\n\n")


# 입력 좌표
# lon_src = 126.978203640984
# lat_src = 37.566585446882
#
# # 변환 (출발지 4326 -> 목적지 4326)
# lon_tgt, lat_tgt = get_espg_transform(
#     lon=lon_src,
#     lat=lat_src,
#     espg_src="EPSG:4326",
#     espg_tgt="EPSG:4326"  # 목적지를 경위도(4326)로 지정
# )
#
# print(f"변환된 좌표 (경도-위도): ({lon_tgt}, {lat_tgt})")
# # 출력 결과는 입력과 거의 같게 나옵니다.
# # 변환된 좌표 (경도-위도): (126.978203640984, 37.566585446882)

def test4():
    # 1. 서울시청의 중부원점 TM 좌표 (EPSG:2097)
    src_x = 126.978203640984  # TM X
    src_y = 37.566585446882  # TM Y

    # 2. 출발지 및 목적지 ESPG 코드 정의 (역변환)
    espg_src_rev = "EPSG:4326"  # 출발지: 중부원점 TM
    espg_tgt_rev = "EPSG:5181"  # 목적지: WGS84 경위도

    # 3. 함수 실행
    lon_rev, lat_rev = get_espg_transform(src_x, src_y, espg_src_rev, espg_tgt_rev)

    # 4. 결과 출력
    print("=" * 80)
    print(f"출발지 좌표 ({espg_src_rev}): (X={src_x:.12f}, Y={src_y:.12f})")
    print(f"목적지 좌표 ({espg_tgt_rev}): (경도={lon_rev:.12f}, 위도={lat_rev:.12f})")
    print("=" * 80)
    print("\n\n\n")



if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()



