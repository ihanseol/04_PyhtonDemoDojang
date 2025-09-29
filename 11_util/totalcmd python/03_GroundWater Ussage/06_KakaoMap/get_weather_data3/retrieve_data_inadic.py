import pandas as pd

DEFAULT_AREA_DATA = [
    {"area": "관악산", "name": "GwanAkSan", "Code": 116, "aCode": 15, "switch": 14},
    {"area": "서울", "name": "Seoul", "Code": 108, "aCode": 16, "switch": 14},
    {"area": "강화", "name": "GangHwa", "Code": 201, "aCode": 24, "switch": 23},
    {"area": "백령도", "name": "BaengNyeongDo", "Code": 102, "aCode": 25, "switch": 23},
    {"area": "인천", "name": "InCheon", "Code": 112, "aCode": 26, "switch": 23},
    {"area": "동두천", "name": "DongDuCheon", "Code": 98, "aCode": 34, "switch": 33},
    {"area": "수원", "name": "SuWon", "Code": 119, "aCode": 35, "switch": 33},
    {"area": "양평", "name": "YangPyung", "Code": 202, "aCode": 36, "switch": 33},
    {"area": "이천", "name": "LeeCheon", "Code": 203, "aCode": 37, "switch": 33},
    {"area": "파주", "name": "PaJu", "Code": 99, "aCode": 38, "switch": 33},
    {"area": "강릉", "name": "GangNeung", "Code": 105, "aCode": 40, "switch": 39},
    {"area": "대관령", "name": "DaeGwallYeong", "Code": 100, "aCode": 41, "switch": 39},
    {"area": "동해", "name": "DongHae", "Code": 106, "aCode": 42, "switch": 39},
    {"area": "북강릉", "name": "NorthGangNeung", "Code": 104, "aCode": 43, "switch": 39},
    {"area": "북춘천", "name": "BukChunCheon", "Code": 93, "aCode": 44, "switch": 39},
    {"area": "삼척", "name": "Samcheok", "Code": 214, "aCode": 45, "switch": 39},
    {"area": "속초", "name": "SokCho", "Code": 90, "aCode": 46, "switch": 39},
    {"area": "영월", "name": "YoungWol", "Code": 121, "aCode": 47, "switch": 39},
    {"area": "원주", "name": "WonJu", "Code": 114, "aCode": 48, "switch": 39},
    {"area": "인제", "name": "InJae", "Code": 211, "aCode": 49, "switch": 39},
    {"area": "정선군", "name": "JungSeonGun", "Code": 217, "aCode": 50, "switch": 39},
    {"area": "철원", "name": "CheolWon", "Code": 95, "aCode": 51, "switch": 39},
    {"area": "춘천", "name": "ChunCheon", "Code": 101, "aCode": 52, "switch": 39},
    {"area": "태백", "name": "TaeBaeg", "Code": 216, "aCode": 53, "switch": 39},
    {"area": "홍천", "name": "HongCheon", "Code": 212, "aCode": 54, "switch": 39},
    {"area": "보은", "name": "BoEun", "Code": 226, "aCode": 56, "switch": 55},
    {"area": "서청주", "name": "SeoCheongJu", "Code": 181, "aCode": 57, "switch": 55},
    {"area": "제천", "name": "JaeCheon", "Code": 221, "aCode": 58, "switch": 55},
    {"area": "청주", "name": "CheongJu", "Code": 131, "aCode": 59, "switch": 55},
    {"area": "추풍령", "name": "ChuPungNyeong", "Code": 135, "aCode": 60, "switch": 55},
    {"area": "충주", "name": "ChungJu", "Code": 127, "aCode": 61, "switch": 55},
    {"area": "대전", "name": "DaeJeon", "Code": 133, "aCode": 30, "switch": 29},
    {"area": "세종", "name": "SeJong", "Code": 239, "aCode": 135, "switch": 134},
    {"area": "금산", "name": "GeumSan", "Code": 238, "aCode": 63, "switch": 62},
    {"area": "보령", "name": "BoRyoung", "Code": 235, "aCode": 64, "switch": 62},
    {"area": "부여", "name": "BuYeo", "Code": 236, "aCode": 65, "switch": 62},
    {"area": "서산", "name": "SeoSan", "Code": 129, "aCode": 66, "switch": 62},
    {"area": "천안", "name": "CheonAn", "Code": 232, "aCode": 67, "switch": 62},
    {"area": "홍성", "name": "HongSung", "Code": 177, "aCode": 68, "switch": 62},
    {"area": "광주", "name": "GwangJu", "Code": 156, "aCode": 28, "switch": 27},
    {"area": "고창", "name": "GoChang", "Code": 172, "aCode": 70, "switch": 69},
    {"area": "고창군", "name": "GochangGun", "Code": 251, "aCode": 71, "switch": 69},
    {"area": "군산", "name": "GunSan", "Code": 140, "aCode": 72, "switch": 69},
    {"area": "남원", "name": "NamWon", "Code": 247, "aCode": 73, "switch": 69},
    {"area": "부안", "name": "BuAn", "Code": 243, "aCode": 74, "switch": 69},
    {"area": "순창군", "name": "SunchangGun", "Code": 254, "aCode": 75, "switch": 69},
    {"area": "임실", "name": "ImSil", "Code": 244, "aCode": 76, "switch": 69},
    {"area": "장수", "name": "JangSoo", "Code": 248, "aCode": 77, "switch": 69},
    {"area": "전주", "name": "JeonJu", "Code": 146, "aCode": 78, "switch": 69},
    {"area": "정읍", "name": "Jungeup", "Code": 245, "aCode": 79, "switch": 69},
    {"area": "강진군", "name": "GangjinGun", "Code": 259, "aCode": 81, "switch": 80},
    {"area": "고흥", "name": "Goheung", "Code": 262, "aCode": 82, "switch": 80},
    {"area": "광양시", "name": "Gwangyang", "Code": 266, "aCode": 83, "switch": 80},
    {"area": "목포", "name": "MokPo", "Code": 165, "aCode": 84, "switch": 80},
    {"area": "무안", "name": "MuAn", "Code": 164, "aCode": 85, "switch": 80},
    {"area": "보성군", "name": "BosungGun", "Code": 258, "aCode": 86, "switch": 80},
    {"area": "순천", "name": "Suncheon", "Code": 174, "aCode": 87, "switch": 80},
    {"area": "여수", "name": "Yeosu", "Code": 168, "aCode": 88, "switch": 80},
    {"area": "영광군", "name": "YeongGwangGun", "Code": 252, "aCode": 89, "switch": 80},
    {"area": "완도", "name": "WanDo", "Code": 170, "aCode": 90, "switch": 80},
    {"area": "장흥", "name": "JangHeung", "Code": 260, "aCode": 91, "switch": 80},
    {"area": "주암", "name": "JuAm", "Code": 256, "aCode": 92, "switch": 80},
    {"area": "진도(첨찰산)", "name": "JinDo", "Code": 175, "aCode": 93, "switch": 80},
    {"area": "진도군", "name": "JinDoGun", "Code": 268, "aCode": 94, "switch": 80},
    {"area": "해남", "name": "HaeNam", "Code": 261, "aCode": 95, "switch": 80},
    {"area": "흑산도", "name": "HeukSanDo", "Code": 169, "aCode": 96, "switch": 80},
    {"area": "대구", "name": "DaeGu", "Code": 143, "aCode": 21, "switch": 20},
    {"area": "대구(기)", "name": "DaeGuGi", "Code": 176, "aCode": 22, "switch": 20},
    {"area": "울산", "name": "WoolSan", "Code": 152, "aCode": 32, "switch": 31},
    {"area": "부산", "name": "BuSan", "Code": 159, "aCode": 18, "switch": 17},
    {"area": "경주시", "name": "GyungJuSi", "Code": 283, "aCode": 98, "switch": 97},
    {"area": "구미", "name": "GuMi", "Code": 279, "aCode": 99, "switch": 97},
    {"area": "문경", "name": "MunGyung", "Code": 273, "aCode": 100, "switch": 97},
    {"area": "봉화", "name": "BongHwa", "Code": 271, "aCode": 101, "switch": 97},
    {"area": "상주", "name": "SangJu", "Code": 137, "aCode": 102, "switch": 97},
    {"area": "안동", "name": "AnDong", "Code": 136, "aCode": 103, "switch": 97},
    {"area": "영덕", "name": "YeongDeok", "Code": 277, "aCode": 104, "switch": 97},
    {"area": "영주", "name": "YeongJu", "Code": 272, "aCode": 105, "switch": 97},
    {"area": "영천", "name": "YeongCheon", "Code": 281, "aCode": 106, "switch": 97},
    {"area": "울릉도", "name": "UlLeungDo", "Code": 115, "aCode": 107, "switch": 97},
    {"area": "울진", "name": "UlJin", "Code": 130, "aCode": 108, "switch": 97},
    {"area": "의성", "name": "UiSeong", "Code": 278, "aCode": 109, "switch": 97},
    {"area": "청송군", "name": "CheongSongGun", "Code": 276, "aCode": 110, "switch": 97},
    {"area": "포항", "name": "PoHang", "Code": 138, "aCode": 111, "switch": 97},
    {"area": "거제", "name": "GeoJae", "Code": 294, "aCode": 113, "switch": 112},
    {"area": "거창", "name": "GeoChang", "Code": 284, "aCode": 114, "switch": 112},
    {"area": "김해시", "name": "KimHaeSi", "Code": 253, "aCode": 115, "switch": 112},
    {"area": "남해", "name": "NamHae", "Code": 295, "aCode": 116, "switch": 112},
    {"area": "밀양", "name": "MilYang", "Code": 288, "aCode": 117, "switch": 112},
    {"area": "북창원", "name": "BukChangWon", "Code": 255, "aCode": 118, "switch": 112},
    {"area": "산청", "name": "SanCheong", "Code": 289, "aCode": 119, "switch": 112},
    {"area": "양산시", "name": "YangSan", "Code": 257, "aCode": 120, "switch": 112},
    {"area": "의령군", "name": "UiRyoung", "Code": 263, "aCode": 121, "switch": 112},
    {"area": "진주", "name": "JinJu", "Code": 192, "aCode": 122, "switch": 112},
    {"area": "창원", "name": "ChangWon", "Code": 155, "aCode": 123, "switch": 112},
    {"area": "통영", "name": "TongYeong", "Code": 162, "aCode": 124, "switch": 112},
    {"area": "함양군", "name": "HamYang", "Code": 264, "aCode": 125, "switch": 112},
    {"area": "합천", "name": "HapCheon", "Code": 285, "aCode": 126, "switch": 112},
    {"area": "고산", "name": "GoSan", "Code": 185, "aCode": 128, "switch": 127},
    {"area": "서귀포", "name": "SeoGuiPo", "Code": 189, "aCode": 129, "switch": 127},
    {"area": "성산", "name": "SungSan", "Code": 188, "aCode": 130, "switch": 127},
    {"area": "성산2", "name": "SungSan2", "Code": 187, "aCode": 131, "switch": 127},
    {"area": "성산포", "name": "SungSanPo", "Code": 265, "aCode": 132, "switch": 127},
    {"area": "제주", "name": "JaeJu", "Code": 184, "aCode": 133, "switch": 127},

    {"area": "전국", "name": "JeonKook", "Code": 0, "aCode": 3, "switch": 2},
    {"area": "서울경기", "name": "SeoulGyungi", "Code": 0, "aCode": 4, "switch": 2},
    {"area": "강원영동", "name": "GangWonEast", "Code": 0, "aCode": 5, "switch": 2},
    {"area": "강원영서", "name": "GangWonWest", "Code": 0, "aCode": 6, "switch": 2},
    {"area": "충북", "name": "ChungBook", "Code": 0, "aCode": 7, "switch": 2},
    {"area": "충남", "name": "ChungNam", "Code": 0, "aCode": 8, "switch": 2},
    {"area": "경북", "name": "GyungBook", "Code": 0, "aCode": 9, "switch": 2},
    {"area": "경남", "name": "GyungNam", "Code": 0, "aCode": 10, "switch": 2},
    {"area": "전북", "name": "JeonBook", "Code": 0, "aCode": 11, "switch": 2},
    {"area": "전남", "name": "JeonNam", "Code": 0, "aCode": 12, "switch": 2},
    {"area": "제주도", "name": "Jejudo", "Code": 0, "aCode": 13, "switch": 2}
]


# 방법 1: next()와 generator expression 사용
def find_area_info_v1(area_data, target_area):
    """
    next()와 generator를 사용한 방법.
    """
    item = next((item for item in area_data if item["area"] == target_area), None)
    if item:
        return {
            "name": item["name"],
            "Code": item["Code"],
            "switch": item["switch"]
        }
    return None


# 사용 예시
result1 = find_area_info_v1(DEFAULT_AREA_DATA, "충남")
print(result1)  # 출력: {'name': 'ChungNam', 'Code': 0, 'switch': 2}


# 방법 2: filter() 함수와 lambda 사용
def find_area_info_v2(area_data, target_area):
    """
    filter()와 lambda를 사용한 방법.
    """
    filtered = list(filter(lambda item: item["area"] == target_area, area_data))
    if filtered:
        item = filtered[0]
        return {
            "name": item["name"],
            "Code": item["Code"],
            "switch": item["switch"]
        }
    return None


# 사용 예시
result2 = find_area_info_v2(DEFAULT_AREA_DATA, "충남")
print(result2)  # 출력: {'name': 'ChungNam', 'Code': 0, 'switch': 2}


# 방법 3: pandas DataFrame으로 변환 후 쿼리 (pandas 필요)

def find_area_info_v3(area_data, target_area):
    """
    pandas DataFrame을 사용한 방법 (pandas 라이브러리 필요).
    """
    df = pd.DataFrame(area_data)
    matched = df[df['area'] == target_area]
    if not matched.empty:
        item = matched.iloc[0]
        return {
            "name": item["name"],
            # "Code": int(item["Code"]),
            "Code": item["Code"],
            # "switch": int(item["switch"])
            "switch": item["switch"]
        }
    return None


# 사용 예시
result3 = find_area_info_v3(DEFAULT_AREA_DATA, "충남")
print(result3)  # 출력: {'name': 'ChungNam', 'Code': 0, 'switch': 2}


# 방법 4: DEFAULT_AREA_DATA를 딕셔너리로 변환 후 .get() 사용
def find_area_info_v4(area_data, target_area):
    """
    DEFAULT_AREA_DATA를 area를 키로 하는 딕셔너리로 변환한 후 .get()을 사용한 방법.
    """
    # area를 키로 하는 딕셔너리 생성
    area_dict = {item["area"]: item for item in area_data}

    # .get()으로 해당 area의 item 가져오기
    item = area_dict.get(target_area)
    if item:
        return {
            "name": item.get("name"),
            "Code": item.get("Code"),
            "switch": item.get("switch")
        }
    return None


# 사용 예시
result4 = find_area_info_v4(DEFAULT_AREA_DATA, "충남")
print(result4)  # 출력: {'name': 'ChungNam', 'Code': 0, 'switch': 2}
