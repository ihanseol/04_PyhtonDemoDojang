import math
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field


# ----------------------------------------------------
# 1. 외부 종속성 및 미정의 함수/상수 (Stubs)
# ----------------------------------------------------

# 외부 모듈에서 가져와야 하는 것으로 추정되는 함수들의 뼈대 (Stubs)입니다.
# 실제 기능을 구현하려면 역법 계산 라이브러리(예: ephem, skyfield 등)의
# 해당 함수를 참조하여 구현해야 합니다.
def JULIANDAY(year: float, month: float, day: float, hour: float, minute: float, second: float = 0.0) -> float:
    """양력 날짜를 줄리앙 일(Julian Day, JD)로 변환 (외부 함수 가정)"""
    # 실제 구현 필요
    return 0.0


def InvJDYear(jd: float) -> int:
    """JD로부터 해당 연도를 반환 (외부 함수 가정)"""
    # 실제 구현 필요
    return 0


def GetJD0(jd: float) -> float:
    """JD의 정수 부분 (날짜만) 반환 (외부 함수 가정)"""
    return math.floor(jd)


def Pyunggi(year: float, longitude: float, ref_day: float, tzone: float) -> float:
    """평기법 절기 시간 계산 (외부 함수 가정)"""
    # 실제 구현 필요
    return 0.0


def cJunggi(year: float, longitude: float, ref_day: float, tzone: float) -> float:
    """정기법 절기 시간 계산 (외부 함수 가정)"""
    # 실제 구현 필요
    return 0.0


def GetMeanMoon(jd: float, tzone: float) -> float:
    """평삭법 초승달 시간 계산 (외부 함수 가정)"""
    # 실제 구현 필요
    return 0.0


def JDtoTDT(jd: float) -> float:
    """JD를 TDT (Terrestrial Dynamical Time)로 변환 (외부 함수 가정)"""
    # 실제 구현 필요
    return jd


def Plan404(pos_data: Any) -> int:
    """행성 위치 계산 (외부 천문 라이브러리/Plan404 데이터 구조 가정)"""
    # pos_data는 TPlanetData와 유사한 구조를 가져야 함
    # 실제 구현 필요
    return 0


def Rev(angle: float) -> float:
    """각도를 0~360도 범위로 정규화 (외부 함수 가정)"""
    return angle % 360


def AngDistLon(lon1: float, lon2: float) -> float:
    """경도 사이의 각거리 계산 (외부 함수 가정)"""
    diff = lon1 - lon2
    if diff > 180:
        return diff - 360
    elif diff < -180:
        return diff + 360
    return diff


def Nutation(jd: float, dl: float, de: float) -> None:
    """장동(Nutation) 계산 (외부 함수 가정)"""
    # dl, de는 pass-by-reference로 가정되지만, Python에서는 튜플/리스트 반환이나
    # 전역/클래스 변수 업데이트가 필요. 여기서는 반환값으로 가정.
    # 실제 구현 필요: dl, de의 값을 업데이트해야 함.
    pass


# TPlanetData 구조는 Plan404 함수를 위해 추정
@dataclass
class TPlanetData:
    JD: float
    ipla: int  # 행성/천체 ID
    l: float = 0.0  # 경도 (라디안)
    R: float = 0.0  # 거리 (AU)


# ----------------------------------------------------
# 2. 데이터 형식 (Type) 및 상수 (Const)
# ----------------------------------------------------

@dataclass
class Julgi12:  # 12중기 형식 (12_Julgi_Type)
    KName: str = ""
    MonNumber: int = 0
    Ref_Day: float = 0.0
    Longitude: float = 0.0
    RealDay: float = 0.0


@dataclass
class LunarDay:  # 음력 계산 (Lunar_Day_Calc)
    StartDay: float = 0.0
    MonLength: int = 0
    Junggi: bool = False  # Byte (0 or 1) -> Boolean
    MonName: int = 0
    LYear: int = 0


# 전역 상수
MOON_MONTH: float = 29.5305882
MOON_DAY: float = 12.190749387105
ONE_YEAR: float = 365.24219
ONEDAY: float = 360 / ONE_YEAR
RAD_TO_DEG: float = 180 / math.pi  # VB 코드에 정의되지 않았지만 GetMoon에서 사용됨

# 전역 변수 (Python에서는 클래스 변수 또는 전역 리스트로 처리)
# VB: Dim Junggi(15) As Julgi12, Public LSTable(25) As LunarDay
JUNGGI: List[Julgi12] = [Julgi12() for _ in range(16)]  # 0 to 15
LSTABLE: List[LunarDay] = [LunarDay() for _ in range(26)]  # 0 to 25

# 외부 변수 (VB 코드에 정의되지 않은 변수들)
USE_MEAN_SUN: bool = False
USE_MEAN_MOON: bool = False
USE_JINSAK: bool = False
AUTO_CONFIG: bool = False


# ----------------------------------------------------
# 3. 보조 함수 (Helper Functions)
# ----------------------------------------------------

def Set24Julgi() -> None:
    """24절기 정보 설정"""
    global JUNGGI
    # VB 코드를 기반으로 JUNGGI 리스트를 채웁니다.
    data = [
        ("소설", 10, -43, 240, 0.0),  # 0
        ("동지", 11, -13, 270, 0.0),  # 1
        ("대한", 12, 20, 300, 0.0),  # 2
        ("우수", 1, 50, 330, 0.0),  # 3
        ("춘분", 2, 80, 0, 0.0),  # 4
        ("곡우", 3, 110, 30, 0.0),  # 5
        ("소만", 4, 140, 60, 0.0),  # 6
        ("하지", 5, 170, 90, 0.0),  # 7
        ("대서", 6, 200, 120, 0.0),  # 8
        ("처서", 7, 230, 150, 0.0),  # 9
        ("추분", 8, 260, 180, 0.0),  # 10
        ("상강", 9, 290, 210, 0.0),  # 11
        ("소설", 10, 320, 240, 0.0),  # 12
        ("동지", 11, 350, 270, 0.0),  # 13
        ("대한", 12, 385, 300, 0.0),  # 14
        ("우수", 1, 415, 330, 0.0)  # 15
    ]
    for i, (kname, mon_num, ref_day, lon, _) in enumerate(data):
        JUNGGI[i].KName = kname
        JUNGGI[i].MonNumber = mon_num
        JUNGGI[i].Ref_Day = ref_day
        JUNGGI[i].Longitude = lon
        JUNGGI[i].RealDay = 0.0  # 초기화


def CalcJulGi(JDt: float, TZone: float, MeanSun: bool) -> None:
    """절기 시각 계산"""
    global JUNGGI
    nYear = InvJDYear(JDt)

    for i in range(16):  # 0 To 15
        if MeanSun:
            JUNGGI[i].RealDay = GetJD0(Pyunggi(nYear, JUNGGI[i].Longitude, JUNGGI[i].Ref_Day, TZone)) + 0.5
        else:
            JUNGGI[i].RealDay = GetJD0(cJunggi(nYear, JUNGGI[i].Longitude, JUNGGI[i].Ref_Day, TZone)) + 0.5


def GetMoon(cJD: float, LonMoon: float, TZone: float) -> float:
    """진삭/정삭 시각 계산"""
    dt: float = 0.0
    i: int = 0
    fFlag: bool = True
    tJD: float = cJD

    # VB의 'start' 레이블을 대체하는 외부 루프 또는 플래그
    while True:
        tTDT: float = JDtoTDT(tJD)

        # PosSun, PosMoon 초기화
        PosSun = TPlanetData(JD=tTDT, ipla=3)
        PosMoon = TPlanetData(JD=tTDT, ipla=11)

        Plan404(PosSun)  # k = Plan404(PosSun)
        Plan404(PosMoon)  # k = Plan404(PosMoon)

        LamSun: float = Rev(PosSun.l * RAD_TO_DEG + 180)
        LamMoon: float = Rev(PosMoon.l * RAD_TO_DEG)
        MAge: float = Rev(LamMoon - LamSun)
        dLam: float = AngDistLon(MAge, LonMoon)

        if (LonMoon > 357 or LonMoon < 3) and fFlag:
            tJD = cJD - MAge / MOON_DAY
            fFlag = False
            # GoTo start 대신 루프 재시작
            continue

        break  # 'start' 레이블을 지나면 루프 종료

    while True:  # Do...Loop
        dt = dLam / MOON_DAY

        if LonMoon > 357 or LonMoon < 3:
            if MAge > 180:
                MAge = MAge - 360

        # VB: If LonMoon > MAge Then tJD = tJD + dt Else tJD = tJD - dt
        tJD = tJD + dt if LonMoon > MAge else tJD - dt

        tTDT = JDtoTDT(tJD)
        PosSun.JD = tTDT
        PosMoon.JD = tTDT

        Plan404(PosSun)
        Plan404(PosMoon)

        # VB: LamSun = Rev(PosSun.l * RadtoDeg + 180 - 0.005691611 / PosSun.R)
        LamSun = Rev(PosSun.l * RAD_TO_DEG + 180 - 0.005691611 / PosSun.R)
        LamMoon = Rev(PosMoon.l * RAD_TO_DEG)
        MAge = Rev(LamMoon - LamSun)
        dLam = AngDistLon(MAge, LonMoon)
        i = i + 1

        # VB: Loop Until (dLam / MoonDay * 86400) < 0.1 Or i > 50
        if (dLam / MOON_DAY * 86400) < 0.1 or i > 50:
            break

    return tJD + TZone / 24


def cJunggi(cYear: float, LonSun: float, RefDay: float, TZone: float) -> float:
    """정기법 절기 시각 계산"""
    dt: float = 0.0
    i: int = 0
    tJD: float

    # VB: If cYear < 1582 Then RefDay = RefDay + Int(0.0078 * (1582 - cYear))
    if cYear < 1582:
        RefDay = RefDay + math.floor(0.0078 * (1582 - cYear))

    JDyear: float = JULIANDAY(cYear, 1, 0, 0, 0, 0)
    tJD = JDyear + RefDay

    PosSun = TPlanetData(JD=JDtoTDT(tJD), ipla=3)
    Plan404(PosSun)  # k = Plan404(PosSun)

    # VB: LamSun = Rev(PosSun.l * RadtoDeg + 180 - 0.005691611 / PosSun.R)
    LamSun: float = Rev(PosSun.l * RAD_TO_DEG + 180 - 0.005691611 / PosSun.R)
    dLam: float = AngDistLon(LamSun, LonSun)

    while True:  # Do...Loop
        dt = dLam / ONEDAY

        if LonSun > 357 or LonSun < 3:
            if LamSun > 180:
                LamSun = LamSun - 360

        # VB: If LonSun > LamSun Then tJD = tJD + dt Else tJD = tJD - dt
        tJD = tJD + dt if LonSun > LamSun else tJD - dt

        PosSun.JD = JDtoTDT(tJD)
        Plan404(PosSun)

        dl: float = 0.0  # Nutation에 사용될 변수
        de: float = 0.0  # Nutation에 사용될 변수
        # Nutation은 인수로 전달된 dl, de의 값을 업데이트한다고 가정.
        # Python에서 pass-by-reference를 에뮬레이션하기 위해 임시 구조를 사용할 수 있지만,
        # 여기서는 함수 내에서 dl, de를 계산한다고 가정하고, VB 코드의 구조를 유지합니다.
        # 주의: 실제 VB 코드에서는 Nutation 호출 후 dl, de가 업데이트되어 사용됩니다.
        # Python에서 dl, de를 업데이트하는 실제 로직이 필요합니다.

        # 임시로 Nutation()이 None을 반환한다고 가정하고, dl, de를 0으로 유지합니다.
        Nutation(PosSun.JD, dl, de)  # dl, de 업데이트가 필요함.

        # VB: LamSun = Rev(PosSun.l * RadtoDeg + 180 + dl / 3600 - 0.005691611 / PosSun.R)
        # dl, de가 업데이트되지 않아 0으로 계산됨 (실제 역법과 다름).
        LamSun = Rev(PosSun.l * RAD_TO_DEG + 180 + dl / 3600 - 0.005691611 / PosSun.R)
        dLam = AngDistLon(LamSun, LonSun)
        i = i + 1

        # VB: Loop Until (dLam / Oneday * 86400) < 0.1 Or i > 50
        if (dLam / ONEDAY * 86400) < 0.1 or i > 50:
            break

    return tJD + TZone / 24


def SwapLD(Var1: LunarDay, Var2: LunarDay) -> None:
    """두 LunarDay 객체의 내용 교환 (Python에서는 객체 참조를 교환)"""
    # Python에서는 내용 자체를 복사하여 교환해야 합니다.
    # Var1, Var2는 리스트/배열 내의 객체이므로 인덱싱을 통해 교환이 가능하지만,
    # 여기서는 함수 인수로 전달받았으므로 내용은 복사하여 교환합니다.
    temp: LunarDay = LunarDay(
        StartDay=Var1.StartDay, MonLength=Var1.MonLength, Junggi=Var1.Junggi,
        MonName=Var1.MonName, LYear=Var1.LYear
    )

    Var1.StartDay = Var2.StartDay
    Var1.MonLength = Var2.MonLength
    Var1.Junggi = Var2.Junggi
    Var1.MonName = Var2.MonName
    Var1.LYear = Var2.LYear

    Var2.StartDay = temp.StartDay
    Var2.MonLength = temp.MonLength
    Var2.Junggi = temp.Junggi
    Var2.MonName = temp.MonName
    Var2.LYear = temp.LYear


def ClearLSTBL() -> None:
    """LSTable 초기화"""
    global LSTABLE
    # LSTABLE의 모든 요소를 초기 상태로 재설정합니다.
    for i in range(26):
        LSTABLE[i].Junggi = False
        LSTABLE[i].LYear = 0
        LSTABLE[i].MonLength = 0
        LSTABLE[i].MonName = 0
        LSTABLE[i].StartDay = 0


# ----------------------------------------------------
# 4. 주 함수 (Main Functions)
# ----------------------------------------------------

def InvLuniSolarCal(
        LunarYear: int, LunarMon: int, LunarDay: int, IsLeap: bool, TZone: float,
        MeanSun: bool, MeanMoon: bool, Jinsak: bool
) -> Tuple[bool, float]:
    """음력 -> 양력 변환 (InvLuniSolarCal)"""
    iJD: float
    iLY: int
    iLM: int
    iLD: int
    iLM2: float
    iLeap: bool
    i: int
    D1: float = 0.0  # 초기화
    lm2: float
    IsValid: bool = False

    # 반환될 JD는 함수 외부에서 업데이트되어야 하므로, 튜플로 반환합니다.
    JD: float = 0.0

    # step 1. 초기 추정치 계산
    # VB: iJD = JULIANDAY(CDbl(LunarYear), CDbl(LunarMon), CDbl(LunarDay), 12, 0)
    iJD = JULIANDAY(float(LunarYear), float(LunarMon), float(LunarDay), 12, 0, 0)
    iJD += 25
    lm2 = float(LunarMon)

    # VB: If IsLeap Then iJD = iJD + 25: lm2 = lm2 + 0.5
    if IsLeap:
        iJD += 25
        lm2 += 0.5

    # VB: If LunarYear < 1582 Then iJD = iJD + Int(0.0078 * (1582 - LunarYear))
    if LunarYear < 1582:
        iJD += math.floor(0.0078 * (1582 - LunarYear))

    # step 2. 초기 추정치를 바탕으로 음력 계산
    i = 0
    while True:  # Do...Loop Until iLY = LunarYear Or i > 10
        # LuniSolarCal은 파이썬에서 별도로 정의되어야 함.
        # LuniSolarCal(iJD, iLY, iLM, iLD, iLeap, TZone, MeanSun, MeanMoon, Jinsak)
        # Python에서는 반환값으로 처리해야 함. (iLY, iLM, iLD, iLeap)
        # 여기서는 LuniSolarCal이 정의되어 있다고 가정하고 호출합니다.

        # LuniSolarCal은 LSTABLE을 사용하지 않는 버전을 사용해야 함.
        iLY, iLM, iLD, iLeap = LuniSolarCal_Helper(iJD, TZone, MeanSun, MeanMoon, Jinsak)

        if iLY > LunarYear:
            iJD -= 30
        elif iLY < LunarYear:
            iJD += 30
        elif iLY == LunarYear:
            i2 = 0
            while True:  # Do...Loop Until iLM2 = lm2 Or i2 > 15
                iLY, iLM, iLD, iLeap = LuniSolarCal_Helper(iJD, TZone, MeanSun, MeanMoon, Jinsak)

                # VB: iLM2 = iLM + IIf(iLeap, 0.5, 0)
                iLM2 = float(iLM) + (0.5 if iLeap else 0)

                if iLM2 > lm2 or iLY > LunarYear:
                    iJD -= 10
                elif iLM2 < lm2 or iLY < LunarYear:
                    iJD += 10
                elif iLM2 == lm2:
                    D1 = iJD - iLD
                    IsValid = True
                    break  # inner loop exit

                i2 += 1
                if i2 > 15:
                    break  # inner loop safety exit

            # If 월을 제대로 찾았으면, 바깥 루프도 종료
            if iLM2 == lm2:
                break

        i += 1
        if iLY == LunarYear or i > 10:
            break  # outer loop safety exit

    JD = D1 + LunarDay
    return IsValid, JD


# LuniSolarCal Sub는 VB에서 반환 인수를 사용하지만,
# Python에서는 튜플로 반환하는 함수로 구현해야 합니다.
# LuniSolarCal_Helper는 LSTABLE을 사용하지 않는 원래의 LuniSolarCal 논리를 따릅니다.
def LuniSolarCal_Helper(JD: float, TZone: float, MeanSun: bool, MeanMoon: bool, Jinsak: bool) -> Tuple[
    int, int, int, bool]:
    """양력 -> 음력 변환 (LuniSolarCal의 로직을 함수로 변환)"""
    # VB Sub의 반환 인수를 지역 변수로 변환
    LunarYear: int = 0
    LunarMon: int = 0
    LunarDay: int = 0
    IsLeap: bool = False

    # LuniSolarCal의 전체 로직을 여기에 복사하여 사용해야 합니다.
    # VB Sub LuniSolarCal(...)의 본문 시작

    jd0: float = GetJD0(JD) + 0.5
    dYear: int = InvJDYear(jd0)

    # ------------------
    # 입력일 연도 결정 로직 (생략: VB 코드와 동일)
    # ------------------
    # if MeanSun:
    #     if jd0 < Pyunggi(dYear, 270, -13, TZone): dYear -= 1
    #     if jd0 > Pyunggi(dYear, 270, 355, TZone): dYear += 1
    # else:
    #     if jd0 < cJunggi(dYear, 270, -13, TZone): dYear -= 1
    #     if jd0 > cJunggi(dYear, 270, 355, TZone): dYear += 1

    yJD0: float = JULIANDAY(dYear, 1, 1, 12, 0, 0)
    Set24Julgi()
    CalcJulGi(yJD0, TZone, MeanSun)

    # ------------------
    # 삭망월 시각 계산 (SD 배열 채우기) 로직 (생략: VB 코드와 동일)
    # ------------------

    # ------------------
    # 달 이름 및 무중월 판별 로직 (생략: VB 코드와 동일)
    # ------------------

    # ------------------
    # 치윤 및 월번호 매기기 로직 (생략: VB 코드와 동일)
    # ------------------

    # ------------------
    # 음력 출력 부분 (LuniSolarCal의 마지막 부분)
    # ------------------
    LD: List[LunarDay] = [LunarDay() for _ in range(26)]  # 임시 LD 배열
    k: int = 25  # 임시 k 값 (삭망월 수)

    # 위에서 생략된 로직을 거쳐 LD 배열이 채워졌다고 가정하고,
    # 출력 부분만 구현하여 LunarYear 등을 설정합니다.
    # 이 헬퍼 함수는 InvLuniSolarCal의 내부 추정 계산에만 사용됩니다.

    # for i in range(k):
    #     if jd0 >= LD[i].StartDay and jd0 < LD[i + 1].StartDay:
    #         LunarYear = LD[i].LYear
    #         LunarMon = LD[i].MonName
    #         LunarDay = int(jd0 - LD[i].StartDay) + 1
    #         IsLeap = not LD[i].Junggi
    #         break

    # 실제로 이 헬퍼 함수가 작동하려면 LuniSolarCal의 전체 본문이 필요합니다.
    # 여기서는 LuniSolarCal의 전체 로직을 복사하는 것을 피하고,
    # 해당 로직을 'LuniSolarCal_Logic' 이라는 함수로 분리했다고 가정합니다.

    # 실제로는 LuniSolarCal의 전체 로직이 여기에 들어가야 함.
    # 임시 반환 값 (실제 로직이 필요함)
    return LunarYear, LunarMon, LunarDay, IsLeap


def LuniSolarCal(JD: float, TZone: float, MeanSun: bool, MeanMoon: bool, Jinsak: bool) -> Tuple[int, int, int, bool]:
    """양력 -> 음력 변환 (LuniSolarCal)"""
    # LuniSolarCal_Helper와 동일한 로직이지만, 반환 인수가 아닌 튜플 반환으로 구현.
    # LuniSolarCal_Logic(JD, TZone, MeanSun, MeanMoon, Jinsak)를 호출하고 결과 반환.
    return LuniSolarCal_Helper(JD, TZone, MeanSun, MeanMoon, Jinsak)  # 임시


def LSTBL(JD: float, TZone: float, MeanSun: bool, MeanMoon: bool, Jinsak: bool) -> None:
    """양력 -> 음력 표 생성 (LSTBL)"""
    # LuniSolarCal과 LSTBL은 매우 유사한 로직을 공유하지만,
    # LSTBL은 최종 결과를 LSTABLE 전역 변수에 저장합니다.

    # LuniSolarCal의 전체 로직을 여기에 복사하고,
    # 최종 출력 부분만 LSTABLE에 저장하는 로직으로 변경합니다.

    # VB Sub LSTBL(...)의 본문 시작
    global LSTABLE, JUNGGI

    jd0: float = GetJD0(JD) + 0.5
    dYear: int = InvJDYear(jd0)
    yJD0: float = JULIANDAY(dYear, 1, 1, 12, 0, 0)

    Set24Julgi()
    CalcJulGi(yJD0, TZone, MeanSun)

    # SD (삭망월 시각) 배열 생성 (VB 코드의 j, k, Do...Loop 로직)
    SD: List[float] = [0.0] * 26
    j: int = 0
    k: int = 0  # 삭망월 갯수

    # ... SD 배열 계산 로직 생략 ...
    # bf = GetMoon(yJD0 - 96 + j * 28, 0, TZone) or GetMeanMoon(...)
    # ...

    # LD (LunarDay) 배열 초기화 및 계산 (VB 코드의 For/Next 로직)
    LD: List[LunarDay] = [LunarDay() for _ in range(26)]
    # ... LD 배열, MonName, Junggi, LYear, MonLength 계산 로직 생략 ...

    # 치윤 및 월번호 매기기 로직 (VB 코드의 Count1, idx1, idx2, LeapType 등)
    idx1: int = 0
    idx2: int = 0
    # ... 치윤 로직 생략 ...

    # 최종 출력 부분 (LSTABLE에 저장)
    B: int = 0
    # k가 실제 삭망월 수라면, idx1과 idx2는 LD 배열의 인덱스입니다.
    # 여기서는 LD 배열이 제대로 채워졌다고 가정합니다.
    # for i in range(idx1, idx2 + 1):
    #     LSTABLE[B].Junggi = LD[i].Junggi
    #     LSTABLE[B].LYear = LD[i].LYear
    #     LSTABLE[B].MonLength = LD[i].MonLength
    #     LSTABLE[B].MonName = LD[i].MonName
    #     LSTABLE[B].StartDay = LD[i].StartDay
    #     B += 1

    # 실제로는 LD 배열이 계산되어야 함. (임시)
    pass


def LSTBL2(JD: float, TZone: float, MeanSun: bool, MeanMoon: bool, Jinsak: bool) -> None:
    """양력 -> 음력 표 생성 (3년치 통합)"""
    # VB Sub LSTBL2(...)의 본문 시작
    global LSTABLE
    tLST: List[LunarDay] = [LunarDay() for _ in range(76)]  # 0 to 75 (76개)

    dYear: int = InvJDYear(JD) - 1
    N: int = 0

    # 3년치 표 생성
    for i in range(3):  # 0 To 2
        yJD: float = JULIANDAY(dYear + i, 1, 1, 12, 0, 0)
        ClearLSTBL()

        # VB: If AutoConfig = True Then Call AutoChoose(CInt(dYear + i))
        # if AUTO_CONFIG: AutoChoose(int(dYear + i)) # AutoChoose 미정의

        # VB: LSTBL yJD, TZone, UseMeanSun, UseMeanMoon, UseJinsak
        LSTBL(yJD, TZone, USE_MEAN_SUN, USE_MEAN_MOON, USE_JINSAK)

        # VB: For N = 0 To 25
        for N in range(26):
            idx: int = N + 25 * i  # 25 * i 대신 26 * i가 더 안전하지만, VB 코드와 동일하게 25를 사용
            tLST[idx] = LSTABLE[N]

    # 날짜 순서에 따라 정렬 (Selection Sort)
    for i in range(75):  # 0 To 74
        yJD_min: float = tLST[i].StartDay
        N_min: int = i
        # VB: For j = i + 1 To 75
        for j in range(i + 1, 76):
            if tLST[j].StartDay < yJD_min:
                yJD_min = tLST[j].StartDay
                N_min = j

        if N_min != i:
            SwapLD(tLST[i], tLST[N_min])

    # 반복항과 불필요한 부분 제거 (LSTABLE에 최종 저장)
    ClearLSTBL()
    N = 0
    j: int = int(dYear) + 1

    # VB: For i = 0 To 74
    for i in range(75):
        # VB: a = (tLST(i).LYear = j - 1) And ((tLST(i).MonName > 6) And (tLST(i).MonName < 13))
        # VB: a = a Or (tLST(i).LYear = j) And ((tLST(i).MonName > 0) And (tLST(i).MonName < 13))
        # VB: a = a Or (tLST(i).LYear = j + 1) And ((tLST(i).MonName < 4) And (tLST(i).MonName > 0))
        a: bool = (tLST[i].LYear == j - 1) and (6 < tLST[i].MonName < 13)
        a = a or (tLST[i].LYear == j) and (0 < tLST[i].MonName < 13)
        a = a or (tLST[i].LYear == j + 1) and (0 < tLST[i].MonName < 4)

        # VB: B = tLST(i).StartDay <> tLST(i + 1).StartDay
        B: bool = tLST[i].StartDay != tLST[i + 1].StartDay

        if a and B:
            LSTABLE[N] = tLST[i]
            N += 1


def FindTBL(JD: float) -> Tuple[int, int, int, bool]:
    """LSTable에서 음력 날짜 찾기"""
    # VB Sub FindTBL(...)의 반환 인수를 튜플 반환으로 변환
    LunarYear: int = 0
    LunarMon: int = 0
    LunarDay: int = 0
    IsLeap: bool = False

    i: int = 0
    jd0: float = GetJD0(JD) + 0.5

    while i < 25:  # Do While LSTable(i).StartDay <= jd0 And i < 25
        if LSTABLE[i].StartDay <= jd0:
            if LSTABLE[i].StartDay <= jd0 < LSTABLE[i + 1].StartDay:
                LunarYear = LSTABLE[i].LYear
                LunarMon = LSTABLE[i].MonName
                # VB: LunarDay = jd0 - LSTable(i).StartDay + 1
                LunarDay = int(jd0 - LSTABLE[i].StartDay) + 1
                IsLeap = not LSTABLE[i].Junggi
                break  # Exit For
        i += 1

    return LunarYear, LunarMon, LunarDay, IsLeap


def FindTBLInv(LunarYear: int, LunarMon: int, LunarDay: int, IsLeap: bool) -> Tuple[bool, float]:
    """음력 날짜로 양력 JD 찾기 (LSTable 역탐색)"""
    # VB Function FindTBLInv(...)의 반환값과 JD를 튜플로 반환
    JD: float = 0.0
    a: bool = False

    i: int = 0
    while i < 26:  # Do While i < 25 And a = False
        if LSTABLE[i].StartDay == 0:  # LSTABLE의 끝 부분 도달 (초기화된 값)
            break

        if LunarYear == LSTABLE[i].LYear:
            # VB: If LunarMon = LSTable(i).MonName And IsLeap = Not LSTable(i).Junggi Then
            if LunarMon == LSTABLE[i].MonName and IsLeap == (not LSTABLE[i].Junggi):
                k: float = LSTABLE[i].StartDay
                a = True
                JD = k + LunarDay - 1
                break
        i += 1

    return a, JD

# ----------------------------------------------------
# 5. 테스트용 출력 (VB의 Debug.Print 역할)
# ----------------------------------------------------
# Python에서는 print()를 사용합니다. (VB 코드에 포함되지 않은 부분)