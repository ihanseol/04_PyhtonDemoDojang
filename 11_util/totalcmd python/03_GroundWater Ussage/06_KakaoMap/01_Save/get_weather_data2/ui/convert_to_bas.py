import os
import datetime
import pandas as pd
import csv

Area = {
    "관악산": "GwanAkSan",
    "서울": "Seoul",
    "강화": "GangHwa",
    "백령도": "BaengNyeongDo",
    "인천": "InCheon",
    "동두천": "DongDuCheon",
    "수원": "SuWon",
    "양평": "YangPyung",
    "이천": "LeeCheon",
    "파주": "PaJu",
    "강릉": "GangNeung",
    "대관령": "DaeGwallYeong",
    "동해": "DongHae",
    "북강릉": "NorthGangNeung ",
    "북춘천": "BukChunCheon",
    "삼척": "Samcheok",
    "속초": "SokCho",
    "영월": "YoungWol",
    "원주": "WonJu",
    "인제": "InJae",
    "정선군": "JungSeonGun",
    "철원": "CheolWon",
    "춘천": "ChunCheon",
    "태백": "TaeBaeg",
    "홍천": "HongCheon",
    "보은": "BoEun",
    "서청주": "SeoCheongJu",
    "제천": "JaeCheon",
    "청주": "CheongJu",
    "추풍령": "ChuPungNyeong",
    "충주": "ChungJu",
    "대전": "DaeJeon",
    "세종": "SeJong",
    "금산": "GeumSan",
    "보령": "BoRyung",
    "부여": "BuYeo",
    "서산": "SeoSan",
    "천안": "CheonAn",
    "홍성": "HongSung",
    "광주": "GwangJu",
    "고창": "GoChang",
    "고창군": "GochangGun",
    "군산": "GunSan",
    "남원": "NamWon",
    "부안": "BuAn",
    "순창군": "SunchangGun",
    "임실": "ImSil",
    "장수": "JangSsoo",
    "전주": "JeonJu",
    "정읍": "Jungeup",
    "강진군": "Gangjingun",
    "고흥": "Goheung",
    "광양시": "Gwangyang",
    "목포": "MokPo",
    "무안": "MuAn",
    "보성군": "BosungGun",
    "순천": "Suncheon",
    "여수": "Yeosu",
    "영광군": "YeongGwangGun",
    "완도": "WanDo",
    "장흥": "JangHeung",
    "주암": "JuAm",
    "진도(첨철산)": "JinDo",
    "진도군": "JinDoGun",
    "해남": "HaeNam",
    "흑산도": "HeukSanDo",
    "대구": "DaeGu",
    "대구(기)": "DaeGuGi",
    "울산": "WoolSan",
    "부산": "BuSan",
    "경주시": "GyungJuSi",
    "구미": "GuMi",
    "문경": "MunGyung",
    "봉화": "BongHwa",
    "상주": "SangJu",
    "안동": "AnDong",
    "영덕": "YeongDeok",
    "영주": "YeongJu",
    "영천": "YeongCheon",
    "울릉도": "UlLeungDo",
    "울진": "UlJin",
    "의성": "UiSeong",
    "청송군": "CheongSongGun",
    "포항": "PoHang",
    "거제": "GeoJae",
    "거창": "GeoChang",
    "김해시": "KimHaeSi",
    "남해": "NamHae",
    "밀양": "MilYang",
    "북창원": "BukChangWon",
    "산청": "SanCheong",
    "양산시": "YangSan",
    "의령군": "UiRyung",
    "진주": "JinJu",
    "창원": "ChangWon",
    "통영": "TongYeong",
    "함양군": "HamYang",
    "합천": "HapCheon",
    "고산": "GoSan",
    "서귀포": "SeoGuiPo",
    "성산": "SungSan",
    "성산2": "SungSan2",
    "성산포": "SungSanPo",
    "제주": "JaeJu"
}


def read_weather_data(fname):
    df = pd.read_csv(fname, skiprows=7, encoding='cp949')
    df.columns = ['date', 'code', 'data']
    data_column = df['data']

    # Add a 'month' column for sorting
    df['month'] = [i % 12 + 1 for i in range(len(df))]

    # Pivot the table
    pivot_df = df.pivot_table(index=df.index // 12, columns='month', values='data', aggfunc='first')

    # Rename the columns with month names
    month_names = [f'{i}월' for i in range(1, 13)]
    pivot_df.columns = month_names

    current_year = datetime.datetime.now().year
    start_year = current_year - 30

    years = range(start_year, start_year + 30)
    pivot_df['year'] = years
    # pivot_df.set_index('year', inplace=True)

    pdf = pivot_df

    # Get the last column name
    last_column = pdf.columns[-1]
    # Move the last column to the first position
    pdf = pdf[[last_column] + [col for col in pdf if col != last_column]]

    # for i in range(len(pdf)):
    #     print(pdf.iloc[i])

    return pdf


def write_bas_data(fname):
    # Extract the area name from the file name
    for korean_name, english_name in Area.items():
        if korean_name in fname:
            eng_area_name = english_name
            break
    else:
        eng_area_name = "Unknown"  # If no match is found

    # Generate the English file name
    eng_fname = eng_area_name + ".bas"

    # Write content to the file
    with open(eng_fname, 'w') as file:
        file.write(f'Function data_{eng_area_name.upper()}() As Variant\n')
        file.write('\n')
        file.write('    Dim myArray() As Variant\n')
        file.write('    ReDim myArray(1 To 30, 1 To 13)\n')
        file.write('\n')

        # Read weather data and write it to the file
        df = read_weather_data(fname)
        for i, row in df.iterrows():
            # list_a = [row[0]] + list(row[1:])  # 이것은 depricated 되었다.
            list_a = [row.iloc[0]] + list(row.iloc[1:])

            print(list_a)
            for j, data in enumerate(list_a, start=1):
                file.write(f"    myArray({i + 1}, {j}) = {data}\n")
                if j % 13 == 0:
                    file.write('\n')

        file.write(f'    data_{eng_area_name.upper()} = myArray\n')
        file.write('\n')
        file.write('End Function\n')


def get_filename():
    download_folder = os.path.expanduser("~\\Downloads\\")
    os.chdir(download_folder)
    files = os.listdir(download_folder)
    files = [file for file in files if file.endswith('.csv')]

    return files


def get_last_line_number_from_file(file_path):
    """
    CSV 파일의 마지막 데이터 라인 번호를 반환합니다.
    파일에 있는 불필요한 설명 부분을 건너뜁니다.

    Args:
        file_path (str): CSV 파일 경로.

    Returns:
        int: 파일의 마지막 데이터 라인 번호. 파일을 찾을 수 없으면 -1을 반환합니다.
    """
    try:
        # 파일의 상단 5줄(설명)과 1개의 공백 라인을 건너뛰기 위해 skiprows=[0, 1, 2, 3, 4, 5]를 지정합니다.
        # 데이터는 7번째 줄부터 시작하며, 첫 줄인 '년월,지점,강수량(mm)'이 헤더입니다.
        df = pd.read_csv(file_path, encoding='cp949', header=0, skiprows=range(6), on_bad_lines='skip',
                         low_memory=False)

        # 데이터프레임이 비어있는지 확인합니다.
        if not df.empty:
            # 마지막 데이터 행의 인덱스를 가져옵니다.
            last_index = df.index[-1]
            # 실제 파일의 라인 번호를 계산합니다.
            # (헤더를 제외한 인덱스) + (건너뛴 라인 수) + (헤더 라인 수)
            # 즉, last_index(0부터 시작) + 1 + 6 = 마지막 데이터 라인 번호
            return last_index + 9
        else:
            return -1  # 유효한 데이터가 없을 경우
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        return -1
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        return -1


def convert_to_vbacode():
    fnames = get_filename()
    if len(fnames) == 0:
        print(".csv file is not found ...")
        return None

    eof_line = 0
    slist = []

    for f in fnames:
        print(f)
        eof_line = get_last_line_number_from_file(f)
        print(f'last number : {eof_line}')
        if eof_line == 368:
            write_bas_data(f)
            slist.append(f)
        else:
            print(f'skip for this is not complete rainfall data : {f}')

    return slist


def test():
    fnames = get_filename()
    if len(fnames) == 0:
        print(".csv file is not found ...")
        exit()

    for f in fnames:
        print(f)
        print(f'last number : {get_last_line_number_from_file(f)}')


def main():
    fnames = get_filename()
    if len(fnames) == 0:
        print(".csv file is not found ...")
        exit()

    eof_line = 0

    for f in fnames:
        print(f)
        eof_line = get_last_line_number_from_file(f)
        print(f'last number : {eof_line}')
        if eof_line == 368:
            write_bas_data(f)
        else:
            print(f'skip for this is not complete rainfall data : {f}')


if __name__ == "__main__":
    # test()
    main()
