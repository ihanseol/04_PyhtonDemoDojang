
"""
양음력 계산 라이브러리 -- Library file for Korean Lunar Calendar
by Senarin
"""

DAY0000 = 1721424.5  # 0000/12/31
SOLAR_EPOCH = 1721425.5  # 0001/1/1
YEAR_MIN = 1583  # Min. Year
YEAR_MAX = 2100  # Max. Year
LUNAR_EPOCH = 2299261.5
LOWER_LIMIT = LUNAR_EPOCH
UPPER_LIMIT = 2488461.5

days_per_month = [31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # Days of the Month

kstems = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]  # 십간 (한글) - Stems (Korean)
hstems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]  # 십간 (한자) - Stems (Hanja)

kbranches = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]  # 십이지 (한글) - Branches (Korean)
hbranches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]  # 십이지 (한자) - Branches (Hanja)

kowkdays = ["일", "월", "화", "수", "목", "금", "토"]  # 한국어 요일명 - Weekdays (Korean)
enwkdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]  # 영문 요일명 - Weekdays (English)



"""

/******************************************************************
 * <음력 데이터 설명>
 * 평달은 작으면: 1, 크면: 2
 * [윤달이 있는 경우]
 * 평달과 윤달이 모두 작으면: 3
 * 평달이 작고 윤달이 크면: 4
 * 평달이 크고 윤달이 작으면: 5
 * 평달과 윤달이 모두 크면: 6
 * [작은달: 29일, 큰달: 30일]
 *
 * <2033년 윤달 문제>
 * 서기 2033년에 윤달을 무중월인 7월에 두어야 할 것인가 동지가 들어있는 11월에 두어야 할 것인가에 대한 문제가 발생함
 * 참고 URL : https://namu.wiki/w/2033%EB%85%84%20%EB%AC%B8%EC%A0%9C
 * 밑의 데이터 중 2033년 부분도 참고 (현재는 현행 만세력에 따라 윤달을 11월로 수정함)
 * 해당 연도의 추석 날짜는 7월에 윤달을 넣는다면 양력 10월 7일이며, 11월에 윤달을 넣는다면 양력 9월 8일이 된다.
 * 일본의 일부 음력 자료는 메톤 주기(Metonic Cycle)에 따라 해당 연도의 음력 11월에 윤달을 두고 있음.
 * (참고로 일본에서 음력은 극소수 일부 분야를 제외하면 거의 쓰이지 않고 있다)
 * 또한 중국 및 베트남의 음력도 해당 연도의 음력 11월에 윤달을 두고 있다.
 ******************************************************************/
"""


 # 1583년 ~ 2100년까지의 자료.
 
lunar_month_tab = [
    [1, 5, 1, 2, 1, 1, 2, 1, 2, 2, 2, 2],  # 1583
    [1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2],
    [1, 2, 2, 1, 1, 2, 1, 1, 5, 2, 2, 1],  # 1585
    [2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 4, 2, 1, 2, 1, 1, 2],
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2],
    [1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 4, 1, 1, 2, 1, 2, 2, 2, 2, 1],  # 1591
    [2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1],
    [2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 5, 2]
]



def solar2JD(year, month, day):
    if month <= 2:
        year -= 1
        month += 12
    
    checksum = (year * 10000) + (month * 100) + day
    a = year // 100
    
    if checksum >= 15821015:
        b = 2 - a + (a // 4)
    elif checksum <= 15821004:
        b = 0
    else:
        return -1
    
    return int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + (b - 1524.5)
    
    
 def JD2solar(jd):
    numdays = int(jd + 0.5)
    
    if numdays < 2299161:
        a = numdays
    else:
        alpha = int((numdays - 1867216.25) / 36524.25)
        a = numdays + 1 + alpha - (alpha // 4)
    
    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(c * 365.25)
    e = int((b - d) / 30.6001)
    
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    day = b - d - int(30.6001 * e)
    
    return [year, month, day]


 def solar2lunar(year, month, day):
    def leap_solar(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    absoluteDay1 = LUNAR_EPOCH - DAY0000
    edays = solar2JD(year, month, day)
    gyear = year if YEAR_MIN <= year <= YEAR_MAX else 0
    
    if gyear == 0:
        return False
    
    days_per_month[1] = 29 if leap_solar(gyear) else 28
    y = gyear - 1
    absoluteDay2 = solar2JD(year, month, day) - DAY0000
    absoluteDay = absoluteDay2 - absoluteDay1 + 1
    
    dt = [0] * (gyear - 1583 + 1)
    for i in range(gyear - 1583 + 1):
        for j in range(12):
            if lunarMonthTab[i][j] == 1:
                daysLunar = 29
            elif lunarMonthTab[i][j] == 2:
                daysLunar = 30
            elif lunarMonthTab[i][j] == 3:
                daysLunar = 58  # 29+29
            elif lunarMonthTab[i][j] == 4:
                daysLunar = 59  # 29+30
            elif lunarMonthTab[i][j] == 5:
                daysLunar = 59  # 30+29
            elif lunarMonthTab[i][j] == 6:
                daysLunar = 60  # 30+30
            dt[i] += daysLunar
    
    p = 0
    while absoluteDay > dt[p]:
        absoluteDay -= dt[p]
        p += 1
    
    q = 0
    isLeap = 0
    while True:
        if lunarMonthTab[p][q] <= 2:
            m0 = lunarMonthTab[p][q] + 28
            if absoluteDay > m0:
                absoluteDay -= m0
                q += 1
            else:
                break
        else:
            if lunarMonthTab[p][q] == 3:
                m1, m2 = 29, 29
            elif lunarMonthTab[p][q] == 4:
                m1, m2 = 29, 30
            elif lunarMonthTab[p][q] == 5:
                m1, m2 = 30, 29
            elif lunarMonthTab[p][q] == 6:
                m1, m2 = 30, 30
            
            if absoluteDay > m1:
                absoluteDay -= m1
                if absoluteDay > m2:
                    absoluteDay -= m2
                    q += 1
                else:
                    isLeap = 1
                    break
            else:
                break
    
    p += 1583
    q += 1
    r = absoluteDay
    lyear, lmonth, lday = p, q, r
    nDays = solar2JD(year, month, day)  # 양력 날짜에 해당하는 율리우스 적일
    syear = (lyear + 6) % 10
    byear = (lyear - 4) % 12
    sbmonth = ((lyear * 12) + lmonth + 13) % 60
    smonth = sbmonth % 10
    bmonth = sbmonth % 12
    sday = int(nDays) % 10
    bday = (int(nDays) + 2) % 12
    
    return [lyear, lmonth, lday, isLeap, nDays, syear, byear, smonth, bmonth, sday, bday]



   def lunar2solar(year, month, day, isLeap):
    def leap_solar(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    lyear = year if YEAR_MIN <= year <= YEAR_MAX else 0
    if lyear == 0:
        return False

    y = lyear - 1583
    m = month - 1
    yleap = 0

    if lunarMonthTab[y][m] > 2:
        if isLeap == 1:
            yleap = 1
            if lunarMonthTab[y][m] in [3, 5]:
                mm = 29
            elif lunarMonthTab[y][m] in [4, 6]:
                mm = 30
        else:
            if lunarMonthTab[y][m] in [1, 3, 4]:
                mm = 29
            elif lunarMonthTab[y][m] in [2, 5, 6]:
                mm = 30

    lday = day
    absoluteDay = 0

    for i in range(y):
        for j in range(12):
            if lunarMonthTab[i][j] == 1:
                absoluteDay += 29
            elif lunarMonthTab[i][j] == 2:
                absoluteDay += 30
            elif lunarMonthTab[i][j] == 3:
                absoluteDay += 58  # 29+29
            elif lunarMonthTab[i][j] == 4:
                absoluteDay += 59  # 29+30
            elif lunarMonthTab[i][j] == 5:
                absoluteDay += 59  # 30+29
            elif lunarMonthTab[i][j] == 6:
                absoluteDay += 60  # 30+30

    for j in range(m):
        if lunarMonthTab[y][j] == 1:
            absoluteDay += 29
        elif lunarMonthTab[y][j] == 2:
            absoluteDay += 30
        elif lunarMonthTab[y][j] == 3:
            absoluteDay += 58  # 29+29
        elif lunarMonthTab[y][j] == 4:
            absoluteDay += 59  # 29+30
        elif lunarMonthTab[y][j] == 5:
            absoluteDay += 59  # 30+29
        elif lunarMonthTab[y][j] == 6:
            absoluteDay += 60  # 30+30

    if yleap == 1:
        if lunarMonthTab[y][m] in [3, 4]:
            absoluteDay += 29
        elif lunarMonthTab[y][m] in [5, 6]:
            absoluteDay += 30

    absoluteDay += lday + 33
    y = 1582

    while True:
        y += 1
        y2 = 366 if leap_solar(y) else 365
        if absoluteDay <= y2:
            break
        absoluteDay -= y2

    gyear = y
    days_per_month[1] = y2 - 337
    m = 0

    while True:
        m += 1
        if absoluteDay <= days_per_month[m - 1]:
            break
        absoluteDay -= days_per_month[m - 1]

    gmonth = m
    gday = absoluteDay
    y = gyear - 1
    nDays = solar2JD(gyear, gmonth, gday)  # 양력 날짜에 해당하는 율리우스 적일
    syear = (year + 6) % 10
    byear = (year - 4) % 12
    sbmonth = ((year * 12) + month + 13) % 60
    smonth = sbmonth % 10
    bmonth = sbmonth % 12
    sday = int(nDays) % 10
    bday = (int(nDays) + 2) % 12

    return [gyear, gmonth, gday, yleap, nDays, syear, byear, smonth, bmonth, sday, bday]




