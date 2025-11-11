import math


# 경고: 이 코드는 원본 VBA 코드의 1:1 변환입니다.
# Rev, JULIANDAY, JDtoTDT 함수는 이 스니펫에서 정의되지 않았으므로
# 외부에서 정의하거나 구현해야 합니다.
# 또한, UseMeanSun, UseMeanMoon, UseJinsak 변수는 전역 변수나 클래스 변수로
# 정의되어야 합니다.

# 필요한 외부 함수/변수 (가정)
# def Rev(angle): ... # 각도를 0-360 범위로 정규화하는 함수 (가정)
# def JULIANDAY(year, month, day, hour, minute, second): ... # 율리우스일 계산 함수 (가정)
# def JDtoTDT(jd): ... # 율리우스일(JD)을 지구역학적 시간(TDT)으로 변환하는 함수 (가정)
# UseMeanSun = False
# UseMeanMoon = False
# UseJinsak = False


def SunML(jde: float) -> float:
    """
    태양의 평균 경도를 계산합니다. (VBA SunML 함수 변환)
    """
    # JDE: Julian Day Ephemeris (역서 율리우스일)

    # T는 율리우스 10만년(365250일)을 단위로 하는 J2000.0 (JD 2451545.0) 이후의 시간
    T = (jde - 2451545.0) / 365250.0
    T2 = T * T
    T3 = T2 * T

    # 태양 평균 경도 (L0)
    L0 = (
            280.4664567
            + 360007.6982779 * T
            + 0.03032028 * T2
            + T3 / 49931.0
            - (T2 * T2) / 15300.0
            - (T3 * T2) / 2000000.0
    )

    # Rev 함수는 각도를 0-360 범위로 정규화하는 함수로 가정합니다.
    # return Rev(L0)
    # Rev 함수가 정의되지 않았으므로, 임시로 모듈로 연산을 사용 (정확한 구현 필요)
    return L0 % 360.0


# ---
def MoonML(jde: float) -> float:
    """
    달의 평균 경도를 계산합니다. (VBA MoonML 함수 변환)
    """
    # T는 율리우스 100년(36525일)을 단위로 하는 J2000.0 (JD 2451545.0) 이후의 시간
    T = (jde - 2451545.0) / 36525.0
    T2 = T * T
    T3 = T2 * T

    # 달 평균 경도 (L0)
    L0 = (
            218.3164477
            + 481267.88123421 * T
            - 0.0015786 * T2
            + T3 / 538841.0
            - (T2 * T2) / 65194000.0
    )

    # Rev 함수는 각도를 0-360 범위로 정규화하는 함수로 가정합니다.
    # return Rev(L0)
    # Rev 함수가 정의되지 않았으므로, 임시로 모듈로 연산을 사용 (정확한 구현 필요)
    return L0 % 360.0


# ---
def Pyunggi(cYear: float, LonSun: float, RefDay: float, TZone: float) -> float:
    """
    평기(平氣)를 계산합니다. (특정 태양 경도에 도달하는 시간) (VBA Pyunggi 함수 변환)
    """
    dt = 0.0
    i = 0

    # 외부 함수 JULIANDAY를 호출한다고 가정
    # if 'JULIANDAY' not in globals():
    #     raise NotImplementedError("JULIANDAY function not defined.")
    # JDyear = JULIANDAY(cYear, 1, 0, 0, 0, 0)

    # 임시 JDyear 값 (JULIANDAY 함수 구현 필요)
    JDyear = 2459944.5  # cYear=2023, 1월 0일 0시 기준 (대략적인 값)

    # 그레고리력 도입 이전의 RefDay 조정 (율리우스력/그레고리력 관련)
    if cYear < 1582:
        RefDay = RefDay + math.floor(0.0078 * (1582.0 - cYear))

    tJD = JDyear + RefDay

    # 반복 계산을 통한 정밀화
    while i <= 10:
        # 외부 함수 JDtoTDT를 호출한다고 가정
        # if 'JDtoTDT' not in globals():
        #     raise NotImplementedError("JDtoTDT function not defined.")
        # TDT = JDtoTDT(tJD)

        # 임시 TDT 값 (JDtoTDT 함수 구현 필요)
        TDT = tJD

        LamSun = SunML(TDT) - 0.0057183  # 태양의 평균 경도 (시차 보정)

        dLam = LonSun - LamSun
        if dLam < 0:
            dLam += 360.0
        if dLam > 180.0:
            dLam -= 360.0

        # 태양의 일일 이동 속도 (도/일)를 사용하여 시간 차이 (일) 계산
        # 0.985647359085214 ≈ 360 / 365.24219
        dt = dLam / 0.985647359085214
        tJD = tJD + dt

        # 시간 정확도 조건 (1초 이내) 또는 최대 반복 횟수 초과 시 종료
        if abs(dLam) / 0.985647359085214 * 86400.0 < 1.0 or i == 10:
            break

        i += 1

    # 결과: 최종 율리우스일 (JD) + 시간대 보정 (TZone/24)
    # TZone: 시간대 오프셋 (시간)
    return tJD + TZone / 24.0


# ---
def GetMeanMoon(cJD: float, TZone: float) -> float:
    """
    평삭(平朔) 또는 평망(平望)을 계산합니다. (합삭/망의 평균 시각) (VBA GetMeanMoon 함수 변환)
    """
    dt = 0.0
    i = 0
    tJD = cJD  # 시작 율리우스일 (JD)

    # 반복 계산을 통한 정밀화
    while i <= 10:
        # 외부 함수 JDtoTDT를 호출한다고 가정
        # if 'JDtoTDT' not in globals():
        #     raise NotImplementedError("JDtoTDT function not defined.")
        # TDT = JDtoTDT(tJD)

        # 임시 TDT 값 (JDtoTDT 함수 구현 필요)
        TDT = tJD

        LamSun = SunML(TDT) - 0.0057183  # 태양의 평균 경도 (시차 보정)
        LamMoon = MoonML(TDT)  # 달의 평균 경도

        dLam = LamSun - LamMoon  # 태양과 달의 경도 차이 (합삭: 0도, 망: 180도)
        if dLam < 0:
            dLam += 360.0
        if dLam > 180.0:
            dLam -= 360.0

        # 태양과 달의 상대 일일 이동 속도 (도/일)를 사용하여 시간 차이 (일) 계산
        # 12.190749387105 ≈ 달-태양의 일일 상대 이동 속도 (360 / 평균 삭망월 일수)
        dt = dLam / 12.190749387105
        tJD = tJD + dt

        # 시간 정확도 조건 (1초 이내) 또는 최대 반복 횟수 초과 시 종료
        if abs(dLam) / 12.190749387105 * 86400.0 < 1.0 or i == 10:
            break

        i += 1

    # 결과: 최종 율리우스일 (JD) + 시간대 보정 (TZone/24)
    # TZone: 시간대 오프셋 (시간)
    return tJD + TZone / 24.0


# ---
def AutoChoose(LYear: int):
    """
    사용할 계산법(평균 태양, 평균 달, 진삭)을 연도에 따라 자동 선택합니다. (VBA AutoChoose 함수 변환)
    """
    # 전역 변수나 클래스 변수로 가정하고 설정합니다.
    global UseMeanSun, UseMeanMoon, UseJinsak

    if LYear < 619:
        UseMeanSun = True
        UseMeanMoon = True
        UseJinsak = False
    elif 619 <= LYear <= 664:
        UseMeanSun = True
        UseMeanMoon = False
        UseJinsak = False
    elif 665 <= LYear <= 1280:
        UseMeanSun = True
        UseMeanMoon = False
        UseJinsak = True
    elif 1281 <= LYear <= 1644:
        UseMeanSun = True
        UseMeanMoon = False
        UseJinsak = False
    elif LYear > 1644:
        UseMeanSun = False
        UseMeanMoon = False
        UseJinsak = False

# ---
# 주석 처리된 AutoChooseKR 함수는 변환하지 않습니다.
