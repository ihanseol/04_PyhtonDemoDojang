import math

# Define constants (though not strictly necessary for this module,
# it's good practice for astronomical code)
# J2000.0 is Julian Day 2451545.0
J2000 = 2451545.0


# --- 1. JULIANDAY: Date (Y/M/D/H/M/S) to Julian Day (JD) ---
def julianday(year: float, month: float, day: float, hour: float, min_val: float, sec: float = 0.0) -> float:
    """
    그레고리력/율리우스력 날짜와 시각을 율리우스 적일(Julian Day, JD)로 변환합니다.
    (VBA: JULIANDAY)

    Args:
        year: 연도 (Year)
        month: 월 (Month)
        day: 일 (Day)
        hour: 시 (Hour)
        min_val: 분 (Minute)
        sec: 초 (Second, Optional)

    Returns:
        율리우스 적일 (JD)
    """

    # 시간(hour)을 소수 일(day)로 변환
    thr = hour + min_val / 60.0 + sec / 3600.0

    # 그레고리력 개혁 적용 여부 (GGG: Gregorian Grid Gate)
    # 1582년 10월 15일(JD 2299161)부터 그레고리력 적용
    ggg = 1.0
    if year < 1582:
        ggg = 0.0
    elif year == 1582:
        if month < 10:
            ggg = 0.0
        elif month == 10 and day < 5:
            ggg = 0.0

    # VBA의 복잡한 그레고리력 보정 계산을 재현

    # J1 부분 계산 시작 (그레고리력 보정 인자)
    # VBA 코드를 따라 Int(7 * (Int((Month + 9) / 12) + Year) / 4) 계산
    # Python에서 정밀도를 위해 math.floor 사용

    # 1. 율리우스력 보정 (JD = JD - Int(7*(Y+M+9)/12 / 4)
    # Note: 이 부분은 율리우스력에서의 윤년 처리와 관련이 있지만,
    # VBA 코드를 1:1로 변환했습니다.
    tjd = -1.0 * math.floor(7.0 * math.floor((month + 9.0) / 12.0 + year) / 4.0)

    # 2. 그레고리력 보정 (a = Int(Y/100), J1 = Int(a/4))
    S = 1.0
    if (month - 9.0) < 0:
        S = -1.0

    a = abs(month - 9.0)
    J1 = math.floor(year + S * math.floor(a / 7.0))
    J1 = -1.0 * math.floor((math.floor(J1 / 100.0) + 1.0) * 3.0 / 4.0)

    tjd += math.floor(275.0 * month / 9.0) + day + (ggg * J1)

    # 1721027: 기원전 4713년 1월 1일 0시의 JD
    # 2 * ggg: 보정 항
    # 367 * Year: 연도 항
    # - 0.5: 자정에서 정오로 기준점 변경
    tjd += 1721027.0 + 2.0 * ggg + 367.0 * year - 0.5

    # 시간 항 추가
    tjd += (thr / 24.0)

    return tjd


# --- 2. InvJD: Julian Day (JD) to Date (Y/M/D/H/M/S) ---
def inv_jd(julday: float) -> tuple[int, int, int, int, int, int]:
    """
    율리우스 적일(JD)을 그레고리력/율리우스력의 날짜와 시각으로 변환합니다.
    (VBA: InvJD)

    Args:
        julday: 율리우스 적일 (JD)

    Returns:
        (Year, Month, Day, Hour, Minute, Second) 튜플
    """

    # JD + 0.5를 정수부 Z와 소수부 f로 분리 (자정 기준)
    Z = math.floor(julday + 0.5)
    f = julday + 0.5 - Z

    # 율리우스력(Z < 2299161) 또는 그레고리력(Z >= 2299161)에 따라 Z를 보정하여 A를 계산
    A = Z
    if Z >= 2299161:
        # 그레고리력 보정
        i = math.floor((Z - 1867216.25) / 36524.25)
        A = Z + 1 + i - math.floor(i / 4.0)

    # 날짜 계산의 시작점(BC 4713년 1월 1일 정오)으로 변환
    B = A + 1524

    # 연도 c
    c = math.floor((B - 122.1) / 365.25)

    # 일수 D (이 해의 3월 1일까지의 대략적인 일수)
    D = math.floor(365.25 * c)

    # 월 T (3월부터 14개월 주기로 계산)
    T = math.floor((B - D) / 30.6)

    # 일(day) 계산
    rj = B - D - math.floor(30.6001 * T) + f
    JJ = int(math.floor(rj))  # Day

    # 시간 계산
    RH = (rj - math.floor(rj)) * 24.0  # Fractional part of day * 24
    hRe = math.floor(RH)  # Hour
    mNe = math.floor((RH - hRe) * 60.0)  # Minute
    sn = math.floor(((RH - hRe) * 60.0 - mNe) * 60.0)  # Second

    # 월(Month) 계산
    mMe = 0
    if T < 14:
        mMe = T - 1
    elif T == 14 or T == 15:
        mMe = T - 13

    # 연도(Year) 계산
    aae = 0
    if mMe > 2:
        aae = c - 4716
    elif mMe == 1 or mMe == 2:
        aae = c - 4715

    # VBA에서는 'Sec'에 CInt(sn)을 사용했으나, Python에서는 정수형으로 반환
    return int(aae), int(mMe), int(JJ), int(hRe), int(mNe), int(sn)


# --- 3. InvJDYear: Julian Day (JD) to Year (only) ---
def inv_jd_year(julday: float) -> float:
    """
    율리우스 적일(JD)을 연도(Year)의 정수 부분만 반환합니다.
    (VBA: InvJDYear)

    Args:
        julday: 율리우스 적일 (JD)

    Returns:
        연도 (Year)의 정수 부분
    """

    # InvJD와 동일한 연도 계산 로직
    Z = math.floor(julday + 0.5)

    A = Z
    if Z >= 2299161:
        i = math.floor((Z - 1867216.25) / 36524.25)
        A = Z + 1 + i - math.floor(i / 4.0)

    B = A + 1524
    c = math.floor((B - 122.1) / 365.25)
    D = math.floor(365.25 * c)
    T = math.floor((B - D) / 30.6)

    mMe = 0
    if T < 14:
        mMe = T - 1
    elif T == 14 or T == 15:
        mMe = T - 13

    if mMe > 2:
        return c - 4716
    elif mMe == 1 or mMe == 2:
        return c - 4715
    return 0.0  # Should not happen


# --- 4. JDtoYear: Julian Day (JD) to Fractional Year ---
def jd_to_year(julday: float) -> float:
    """
    율리우스 적일(JD)을 소수점 연도(Fractional Year)로 변환합니다.
    (VBA: JDtoYear)

    Args:
        julday: 율리우스 적일 (JD)

    Returns:
        소수점 연도 (e.g., 2000.5)
    """

    # 현재 JD에 해당하는 정수 연도 (CY)를 구함
    CY = math.floor(inv_jd_year(julday))

    # 해당 연도의 시작점 JD (1월 1일 12시)
    SY = julianday(CY, 1, 1, 12, 0)

    # 다음 연도의 시작점 JD (CY+1년 1월 1일 12시)
    eY = julianday(CY + 1, 1, 1, 12, 0)

    # 소수 연도 계산: fY = (현재 JD - 연도 시작 JD) / (1년의 JD 일수)
    # VBA의 JulianDay 함수는 정오(12시)를 기준으로 하므로, SY와 eY도 정오 기준
    fY = (julday - SY) / (eY - SY)

    return CY + fY


# --- 5. GetJD0: Get Julian Day at previous/next Noon (0.5) ---
def get_jd0(date_jd: float) -> float:
    """
    주어진 JD에 가장 가까운 율리우스 적일의 0.5 시점(정오)을 반환합니다.
    (VBA: GetJD0)

    Args:
        date_jd: 율리우스 적일 (JD)

    Returns:
        가장 가까운 JD.5 값
    """
    # JD의 소수부 (시간 부분)
    frac_part = date_jd - math.floor(date_jd)

    if frac_part >= 0.5:
        # 소수부가 0.5 이상이면 다음 JD의 0.5 (정오)
        return math.floor(date_jd) + 0.5
    else:
        # 소수부가 0.5 미만이면 이전 JD의 0.5 (정오)
        return math.floor(date_jd) - 0.5


# --- 6. chkJD: Check if JD matches a given Y/M/D/H/M (excluding Sec) ---
def chk_jd(julday: float, YY: float, MM: float, DD: float, hr: float, mn: float, ss: float = 0.0) -> bool:
    """
    JD를 변환한 날짜가 주어진 날짜/시간과 일치하는지 확인합니다. (초는 무시)
    (VBA: chkJD)

    Args:
        julday: 율리우스 적일 (JD)
        YY, MM, DD, hr, mn, ss: 확인할 날짜/시간

    Returns:
        일치 여부 (True/False)
    """

    # InvJD로 JD를 날짜/시간으로 변환
    a, B, c, D, E, f = inv_jd(julday)

    # VBA 코드에서 초(f)가 30초 이상이면 분(E)을 올림 처리
    E_adjusted = E
    if f >= 30:
        E_adjusted += 1

    # 반올림된 분이 60이면 시를 올림 처리 (VBA 코드에 명시되진 않았으나 논리적 가정)
    if E_adjusted == 60:
        D += 1
        E_adjusted = 0

    # 비교: 연/월/일/시/분만
    return YY == a and MM == B and DD == c and hr == D and mn == E_adjusted


# --- 7. MakeTimeString: Format time string (Hour only, e.g., "(05시)") ---
def make_time_string(julday: float) -> str:
    """
    JD를 (시) 형식의 문자열로 반환합니다. 분은 반올림하여 시에 반영합니다.
    (VBA: MakeTimeString)

    Args:
        julday: 율리우스 적일 (JD)

    Returns:
        (시) 형식의 문자열 (e.g., "(05시)")
    """

    pY, pm, pd, PH, pmn, ss = inv_jd(julday)

    # 초를 분에 더하고 분을 60으로 나누어 올림 (VBA의 Round 함수는 4.5 -> 4, 5.5 -> 6의 짝수 반올림을 사용하지 않음)
    # VBA의 Round(x / 60)은 (x / 60)을 반올림함.
    # pmn + ss / 60: 분 + 초/60
    # (pmn + ss / 60) / 60: 이 값을 시 단위로 변환
    # Round((pmn + ss / 60) / 60): 시 단위로 반올림된 값이 나옴. (예: 0.1시간 -> 0, 0.9시간 -> 1)
    # 이 반올림된 값을 PH에 더함.

    # VBA 코드를 따라 pmn을 시 단위로 변환 후 반올림하여 PH에 더하는 방식
    pmn_hours_rounded = round((pmn + ss / 60.0) / 60.0)
    PH += pmn_hours_rounded

    # 시간(PH)을 24를 넘으면 24로 나눈 나머지로 변환 (VBA에서는 처리되지 않았으나, 시간 표현의 일반적인 규칙)
    PH = PH % 24

    PH_str = str(int(PH))

    # 문자열 포맷팅
    if PH < 10:
        return f"(0{PH_str}시)"
    else:
        return f"({PH_str}시)"


# --- 8. MakeTimeString3: Format time string (H:M, e.g., "05:30") ---
def make_time_string3(julday: float) -> str:
    """
    JD를 시:분 형식의 문자열로 반환합니다. 초는 분에 반올림하여 반영합니다.
    (VBA: MakeTimeString3)

    Args:
        julday: 율리우스 적일 (JD)

    Returns:
        시:분 형식의 문자열 (e.g., "05:30")
    """

    pY, pm, pd, PH, pmn, ss = inv_jd(julday)

    # 초를 분에 더한 후 반올림 (VBA의 Round 사용)
    pmn_rounded = round(pmn + ss / 60.0)

    pmn_final = int(pmn_rounded)
    PH_final = int(PH)

    if pmn_final == 60:
        PH_final += 1
        pmn_final = 0

    # PH가 24를 넘을 경우 0으로 리셋 (VBA에서는 처리되지 않았으나, 시간 표현의 일반적인 규칙)
    if PH_final == 24:
        PH_final = 0

    # 문자열 포맷팅 (두 자릿수 맞추기)
    PH_str = str(PH_final).zfill(2)
    pmn_str = str(pmn_final).zfill(2)

    return f"{PH_str}:{pmn_str}"


# --- 9. MakeTimeString4: Format date string (Y년M월D일, e.g., "2000년1월1일") ---
def make_time_string4(julday: float) -> str:
    """
    JD를 연월일 형식의 문자열로 반환합니다. (기원전/후 포함)
    (VBA: MakeTimeString4)

    Args:
        julday: 율리우스 적일 (JD)

    Returns:
        연월일 형식의 문자열 (e.g., "기원전 4712년1월1일")
    """

    pY, pm, pd, PH, pmn, ss = inv_jd(julday)

    pY_int = int(pY)

    # 연도 포맷팅
    if pY_int <= 0:
        # 기원전 (BC) 연도: -1년은 기원전 2년, 0년은 기원전 1년
        tYear = f"기원전 {abs(pY_int) + 1}"
    else:
        tYear = str(pY_int)

    # 문자열 포맷팅
    return f"{tYear}년{int(pm)}월{int(pd)}일"
