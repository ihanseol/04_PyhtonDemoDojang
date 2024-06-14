from pyproj import Proj, transform, Transformer


class Table_dataframe:

    def __init__(self):
        self.lonx = []
        self.laty = []
        self.grade = []

    def proj_df2(self, df2, designated, csv):
        # 좌표 변환 코드
        p1 = Proj(
            "+proj=tmerc +lat_0=38 +lon_0=127.5 +k=0.9996 +x_0=1000000 +y_0=2000000 +ellps=GRS80 +units=m +no_defs")
        p2 = Proj(proj='latlong', datum='WGS84')

        for i in range(len(df2['X 좌표'])):
            lon, lat, z = transform(p1, p2, df2['X 좌표'].values[i], df2['Y 좌표'].values[i], 0.0)
            self.lonx.append(lon)
            self.laty.append(lat)

        df2['위도'] = self.laty
        df2['경도'] = self.lonx

        if ('E_SIG_NAME' in csv.columns) or ('e_sig_name' in csv.columns):
            df2['시군구명'] = csv['E_SIG_NAME']
            df2['행정동명'] = csv['E_EMD_NAME']
            df2 = df2[['시군구명', '행정동명', designated, 'X 좌표', 'Y 좌표', '위도', '경도']]
        else:
            df2['시군구명'] = None
            df2['행정동명'] = None
            df2 = df2[['시군구명', '행정동명', designated, 'X 좌표', 'Y 좌표', '위도', '경도']]

        return df2


def trans_coord_ver1(coord_x, coord_y):
    transformer = Transformer.from_crs("epsg:4326", "epsg:5186")
    point = [coord_x, coord_y]
    trans_coord = transformer.transform(point[0], point[1])
    return trans_coord


def trans_coord_ver2(coord_x, coord_y):
    proj_4326 = Proj(init='epsg:4326')
    proj_5186 = Proj(init='epsg:5186')

    lon, lat = transform(proj_4326, proj_5186, coord_x, coord_y)
    return lon, lat


"""

경위도 좌표가 TM 좌표로 잘 변환이 된다.
위경도 , 이렇게 좌표값을 넣어야 하고
반환된 값 (417942.1599999986, 230058.07999997822)

는 AutoCad 에서, 230058.07999997822, 417942.1599999986 이렇게 넣어 주어야 한다.

"""
# print(trans_coord_ver1(36.3590896879659, 127.334896600034))

#세종시 에머슨 골프장
print(trans_coord_ver1(36.6910321, 127.1756172))




