from datetime import date, timedelta

# 원본 kor-lunar-js의 LUNAR_DATA 배열을 딕셔너리로 변환 (2020년 ~ 2050년)
# {연도: [윤달 월 (0: 없음), 1월 일수, 2월 일수, ..., 12월 일수]}
LUNAR_DATA = {
    2020: [4, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
    2021: [0, 29, 30, 29, 30, 29, 30, 29, 30, 30, 29, 30, 30],
    2022: [0, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29],
    2023: [2, 30, 29, 30, 30, 29, 30, 29, 30, 29, 30, 29, 30],
    2024: [0, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30, 29, 30],
    2025: [0, 30, 29, 30, 30, 29, 30, 29, 30, 29, 30, 29, 30],
    2026: [6, 30, 29, 30, 29, 30, 29, 30, 30, 29, 30, 29, 30],
    2027: [0, 29, 30, 29, 30, 29, 30, 29, 30, 30, 29, 30, 29],
    2028: [0, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30, 29, 30],
    2029: [3, 30, 29, 30, 29, 30, 30, 29, 30, 29, 30, 29, 30],
    2030: [0, 29, 30, 29, 30, 29, 30, 29, 30, 30, 29, 30, 29],
    2031: [0, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30, 29, 30],
    2032: [7, 30, 29, 30, 29, 30, 29, 30, 30, 29, 30, 29, 30],
    2033: [0, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30, 29],
    2034: [0, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30],
    2035: [5, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29],
    2036: [0, 30, 29, 30, 30, 29, 30, 29, 30, 29, 30, 29, 30],
    2037: [0, 30, 29, 30, 29, 30, 30, 29, 30, 29, 30, 29, 30],
    2038: [2, 29, 30, 29, 30, 29, 30, 29, 30, 30, 29, 30, 29],
    2039: [0, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30, 29, 30],
    2040: [0, 30, 29, 30, 29, 30, 30, 29, 30, 29, 30, 29, 30],
    2041: [6, 29, 30, 29, 30, 29, 30, 29, 30, 30, 29, 30, 30],
    2042: [0, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30],
    2043: [0, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30, 29, 30],
    2044: [3, 30, 29, 30, 29, 30, 29, 30, 30, 29, 30, 29, 30],
    2045: [0, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30, 29],
    2046: [0, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 30],
    2047: [7, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29],
    2048: [0, 30, 30, 29, 30, 29, 30, 29, 30, 29, 30, 29, 30],
    2049: [0, 30, 29, 30, 30, 29, 30, 29, 30, 29, 30, 29, 30],
    2050: [4, 29, 30, 29, 30, 29, 30, 30, 29, 30, 29, 30, 29],
}

# 기준일: 2020년 1월 25일 (음력 2020년 1월 1일)
# JavaScript 원본 코드의 baseYear/baseDate와 유사한 기준점
BASE_DATE_SOLAR = date(2020, 1, 25)
BASE_YEAR_LUNAR = 2020


def sol2lunar(year: int, month: int, day: int) -> dict:
    """
    양력(Solar) 날짜를 음력(Lunar) 날짜로 변환합니다.
    (2020년 ~ 2050년 범위)
    """
    try:
        current_date_solar = date(year, month, day)
    except ValueError:
        return {"error": "Invalid Solar Date"}

    if not (BASE_YEAR_LUNAR <= year <= max(LUNAR_DATA.keys())):
        return {"error": "Date out of range (2020~2050)"}

    # 1. 기준일로부터 총 일수 계산
    # 음력 2020년 1월 1일(양력 2020/1/25)부터 입력된 양력 날짜까지의 일수
    days_since_base = (current_date_solar - BASE_DATE_SOLAR).days

    # 2. 음력 날짜 찾기
    lunar_year = BASE_YEAR_LUNAR

    while True:
        if lunar_year not in LUNAR_DATA:
            return {"error": "LUNAR_DATA not available for this year"}

        # 해당 음력 연도의 전체 일수를 계산합니다.
        # LUNAR_DATA[year]의 0번째 요소는 윤달 정보, 1번째부터 12월까지 일수
        # 윤달이 있다면 윤달 일수(LUNAR_DATA[year][LUNAR_DATA[year][0] + 1])가 포함됨.
        days_in_lunar_year = sum(LUNAR_DATA[lunar_year][1:])

        # 전체 일수보다 days_since_base가 작으면 이 해에 날짜가 존재
        if days_since_base < days_in_lunar_year:
            break

        # 크거나 같으면 다음 해로 이동
        days_since_base -= days_in_lunar_year
        lunar_year += 1

        if lunar_year > max(LUNAR_DATA.keys()):
            return {"error": "Date out of range (2020~2050)"}

    # 3. 음력 월/일 찾기
    lunar_month = 1
    is_leap_month = False

    # LUNAR_DATA[lunar_year] = [윤달 월, 1월 일수, ..., 12월 일수]
    lunar_data = LUNAR_DATA[lunar_year]

    # 1월부터 순회하며 날짜 찾기
    for i in range(1, 13):
        days_in_month = lunar_data[i]

        # 윤달 처리
        if i == lunar_data[0]:
            # 윤달 일수 (i는 윤달의 실제 월을 가리키므로, 다음 인덱스 i+1이 윤달의 일수)
            # 단, Python 포팅 시 LUNAR_DATA 구조를 [윤달 월, 1월 일수, ..., 12월 일수]로 했으므로,
            # 윤달 월의 일수는 lunar_data[i]가 아닌, 윤달이 삽입되는 위치의 다음 월 일수를 사용해야 함.
            # 하지만 원본 JS 코드를 참고하여 여기서는 1월부터 순차적으로 일수를 계산합니다.

            # 음력 월 (lunar_month)이 윤달이 끼는 월과 같을 경우
            if lunar_month == lunar_data[0]:
                days_in_leap_month = lunar_data[lunar_data[0] + 1]

                # 윤달에 날짜가 포함되는 경우
                if days_since_base < days_in_leap_month:
                    is_leap_month = True
                    lunar_day = days_since_base + 1
                    return {
                        "year": lunar_year,
                        "month": lunar_month,
                        "day": lunar_day,
                        "is_leap_month": is_leap_month
                    }

                # 윤달을 지나서 평달로 넘어가는 경우
                days_since_base -= days_in_leap_month

        # 평달 일수
        if days_since_base < days_in_month:
            lunar_day = days_since_base + 1
            return {
                "year": lunar_year,
                "month": lunar_month,
                "day": lunar_day,
                "is_leap_month": False
            }

        days_since_base -= days_in_month
        lunar_month += 1

    # 만약 위의 루프에서 반환되지 않았다면 오류
    return {"error": "Conversion error"}
