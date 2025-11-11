import math
from typing import List, Dict, Any

# --- Assumed External Dependencies (Must be replaced with actual logic) ---

# TimeZone: Assume a global time zone offset in hours (e.g., 9 for KST)
# Note: The original VBA code uses TimeZone directly in cJunggi,
# which usually takes a decimal hour offset.
TimeZone = 9.0
UseMeanSun = True
UseMeanMoon = True
UseJinsak = False


# Dummy/Placeholder Functions from previous context or external modules
def julianday(year: float, month: float, day: float, hour: float, min_val: float, sec: float = 0.0) -> float:
    # Placeholder: Replace with the actual julianday function logic
    # (The JD function provided in the previous turn should be used here)
    return 0.0


def get_jd0(date_jd: float) -> float:
    # Placeholder: Replace with the actual GetJD0 function logic
    # Finds the Julian Day at the nearest noon (.5)
    if date_jd - math.floor(date_jd) >= 0.5:
        return math.floor(date_jd) + 0.5
    else:
        return math.floor(date_jd) - 0.5


def rev(angle: float) -> float:
    # Placeholder: Replace with the actual Rev function logic (angle modulation 0-360)
    return angle % 360.0


def c_junggi(year: float, longitude: float, start_lon: float, time_zone: float) -> float:
    # Placeholder: Calculates Julian Day for a specific Solar Term (Junggi/Jeolgi)
    # This function is crucial for HANSHEK and SAMBOK, requiring precise solar calculation.
    return 0.0  # Must be implemented


def inv_luni_solar_cal(year: int, month: int, day: int, leap: bool, tz: float, use_mean_sun: bool, use_mean_moon: bool,
                       use_jinsak: bool, out_jd: float) -> bool:
    # Placeholder: Calculates solar date (JD) from lunar date (InvLuniSolarCal)
    # This is required for calculating Seolnal (Lunar New Year).
    # Since Python cannot pass 'out_jd' by reference, we assume it returns the JD.
    # Return JD if successful, 0.0 if not.
    return 0.0


def find_tbl_inv(year: int, month: int, day: int, leap: bool, out_jd: float) -> bool:
    # Placeholder: Alternative lunar-to-solar date conversion function (FindTBLInv)
    return False


def make_time_string(julday: float) -> str:
    # Placeholder: Formats time string. Replace with the actual MakeTimeString function.
    return "TIME_STR"


# --- SpecialDay Type and Global Array Simulation ---

# VBA Type SpecialDay structure simulated using a dictionary
class SpecialDay:
    def __init__(self):
        self.RealDay = 0.0
        self.y = -10000  # Default sentinel value in VBA code
        self.M = -5  # Default sentinel value in VBA code
        self.D = 0
        self.LuniSolar = False
        self.LeapMonth = False
        self.DayName = ""
        self.Holy = 0  # 0: None, 1: Minor Holiday, 2: Major Holiday, 3: Both


# Global array simulation
SDay: List[SpecialDay] = [SpecialDay() for _ in range(201)]


# --- Helper Functions ---

def clear_s_day():
    """VBA의 ClearSDay Sub를 1:1 변환"""
    global SDay
    for i in range(201):
        SDay[i] = SpecialDay()


def read_day_data():
    """
    VBA의 ReadDayData Sub를 1:1 변환.
    Sheet2 데이터 로딩 부분을 더미 데이터 로딩으로 대체합니다.
    실제 사용 시에는 엑셀/CSV 등에서 데이터를 읽어와야 합니다.
    """
    global SDay

    # Placeholder for Sheet2 data: Mimic reading 10 sample rows
    # Structure: [y, M, D, Leap?, LuniSolar?, Holy, DayName]
    dummy_data = [
        [-10000, 3, 1, "", "", 1, "삼일절"],  # Solar: 3/1
        [-10000, 8, 15, "", "", 1, "광복절"],  # Solar: 8/15
        [-10000, 1, 1, "y", "y", 2, "설날"],  # Lunar: 1/1
        [-10000, 8, 15, "", "y", 2, "추석"],  # Lunar: 8/15
        [2024, 12, 25, "", "", 2, "크리스마스"]  # Fixed Year Solar Day
    ]

    for idx, row in enumerate(dummy_data):
        if idx >= 150:
            break

        s_day = SDay[idx]
        y_val, M_val, D_val, leap_str, luni_str, Holy_val, DayName_val = row

        # VBA: Sheet2.Cells(Num, 1).Value -> .y
        if str(y_val).strip() == "":
            s_day.y = -10000
        elif str(y_val).strip() == "x":
            s_day.y = -15000
        else:
            s_day.y = int(y_val)

        s_day.M = int(M_val)
        s_day.D = int(D_val)
        s_day.LeapMonth = leap_str.strip() != ""
        s_day.LuniSolar = luni_str.strip() != ""
        s_day.Holy = int(Holy_val)
        s_day.DayName = str(DayName_val).strip()

    # Set the sentinel value for the next unused entry (VBA: Num - 2)
    if len(dummy_data) < 201:
        SDay[len(dummy_data)].M = -5  # Sentinel


# --- Core Functions ---

def find_easter(y: int) -> float:
    """
    VBA의 FindEaster Function을 1:1 변환 (부활절 JD 계산).
    (Gregorian/Julian method based on year)
    """

    mon: float
    Da: float

    if y >= 1583:
        # Gregorian Easter Calculation (Meeus/Butcher's Algorithm)
        a = y % 19
        B = y // 100
        c = y % 100
        D = B // 4
        E = B % 4
        f = (B + 8) // 25
        g = (B - f + 1) // 3
        h = (19 * a + B - D - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * E + 2 * i - h - k) % 7
        M = (a + 11 * h + 22 * l) // 451
        N = (h + l - 7 * M + 114) // 31
        P = (h + l - 7 * M + 114) % 31

        mon = float(N)
        Da = float(P + 1)
    else:
        # Julian Easter Calculation (Gauss's simple rule for Julian calendar)
        a = y % 4
        B = y % 7
        c = y % 19
        D = (19 * c + 15) % 30
        E = (2 * a + 4 * B - D + 34) % 7
        f = (D + E + 114) // 31
        g = (D + E + 114) % 31

        mon = float(f)
        Da = float(g + 1)

    return julianday(float(y), mon, Da, 12.0, 0.0)


def get_other_day(kind: int, c_year: int) -> float:
    """
    VBA의 GetOtherDay Function을 1:1 변환 (한식, 삼복, 부활절 등 계산).
    """
    j = 0.0
    R = 0.0

    if kind == 0:  # 한식 (HANSHEK): 동지(전년) 다음 날로부터 105일째 날
        pY = c_year - 1
        # cJunggi(270) = 동지 (Winter Solstice)
        j = c_junggi(float(pY), 270.0, 350.0, TimeZone)
        j = get_jd0(j) + 0.5  # 정오 JD.5
        R = j + 105

    elif kind == 1:  # 초복 (CHOBOK)
        # cJunggi(90) = 하지 (Summer Solstice)
        j = c_junggi(float(c_year), 90.0, 170.0, TimeZone)
        j = get_jd0(j) + 0.5

        # 4번째 경일 (4th Gyeong day) 찾기
        N = (j + 49) % 60  # 하지 JD의 간지 번호 (JD 1일 = 갑자(0), 49: 49일 후의 간지)
        M = N % 10  # N에서 10을 나눈 나머지 (M=0: 甲, M=1: 乙, ..., M=6: 庚)

        # 첫 번째 경일 (庚日)까지의 일수 (M=6)
        if M <= 6:
            j += (6 - M)
        else:  # M=7, 8, 9 (辛, 壬, 癸)
            j += (16 - M)  # 다음 경일은 10+6-M 일 후

        R = j + 20  # 3번째 경일(10일) + 10일 = 4번째 경일. 초복은 4번째 경일

    elif kind == 2:  # 중복 (JUNGBOK): 5번째 경일
        # 하지 JD 계산 및 3번째 경일(j)까지의 로직은 초복과 동일
        j = c_junggi(float(c_year), 90.0, 170.0, TimeZone)
        j = get_jd0(j) + 0.5
        N = (j + 49) % 60
        M = N % 10

        if M <= 6:
            j += (6 - M)
        else:
            j += (16 - M)

        R = j + 30  # 3번째 경일(j) + 20일 + 10일 = 5번째 경일. 중복은 5번째 경일

    elif kind == 3:  # 말복 (MALBOK)
        # cJunggi(135) = 입추 (Lichu/Start of Autumn)
        j = c_junggi(float(c_year), 135.0, 215.0, TimeZone)
        j = get_jd0(j) + 0.5

        # 입추 JD의 3번째 경일(j)까지의 로직 (입추 JD의 첫 번째 경일)
        N = (j + 49) % 60
        M = N % 10

        if M <= 6:
            j += (6 - M)
        else:
            j += (16 - M)

        R = j  # 입추 JD 이후 첫 번째 경일. 말복은 입추 JD 이후 첫 번째 경일 (4번째 or 5번째 경일)

    elif kind == 4:  # 납향 (NAPHYANG)
        pY = c_year - 1
        # 동지 (전년)
        j = c_junggi(float(pY), 270.0, 350.0, TimeZone)
        j = get_jd0(j) + 0.5

        # 동지 후 3번째 戌일 (Sul day) 찾기 (N = 戌: 49-2 = 47)
        N = (j + 49) % 60
        M = N % 12  # M=0: 子, M=1: 丑, ..., M=10: 戌

        # 첫 번째 술일(M=10)까지의 일수
        if M <= 10:
            j += (10 - M)
        else:  # M=11 (亥)
            j += (22 - M)  # 다음 술일은 12+10-M 일 후

        R = j + 24  # 첫 번째 술일(j) + 12일 + 12일 = 3번째 술일

    elif kind == 5:  # 제석 (JESEOK): 설날 전날
        # InvLuniSolarCal(cYear, 1, 1, False) = 설날 (Lunar New Year)
        # j is the JD of Lunar New Year
        j = inv_luni_solar_cal(c_year, 1, 1, False, TimeZone, UseMeanSun, UseMeanMoon, UseJinsak, 0.0)
        R = j - 1.0

    elif kind == 6:  # 부활절 (EASTER)
        R = find_easter(c_year)

    elif kind == 7:  # 성년의 날 (Coming-of-Age Day): 5월 셋째 주 월요일
        # 5월 1일의 JD를 구함
        j = julianday(float(c_year), 5.0, 1.0, 12.0, 0.0)

        # 5월 1일의 요일 (JD 0 = 월요일, Mod 7: 0=월, 1=화, ..., 6=일)
        # 참고: VBA의 Mod 7 결과는 0..6 이므로 0=일요일, 1=월요일...일 가능성도 있으나,
        # 일반적인 JD 요일 계산 (JD.5 mod 7)은 0=월요일, 1=화요일... 6=일요일
        # VBA 코드를 따라 N=(j+1) Mod 7 -> N=0:일, 1:월, 2:화, ... 6:토 (가정)
        N = int((j + 1) % 7)

        # 5월 1일부터 첫 번째 월요일(N=1)까지의 일수 (M)
        M = 0
        if N <= 1:  # 5/1이 일요일(0) 또는 월요일(1)인 경우
            M = 1 - N  # 0 또는 1
        else:  # 5/1이 화요일(2) ~ 토요일(6)인 경우
            M = 8 - N  # 6 ~ 2

        # 5월 첫 번째 월요일 = j + M
        # 5월 셋째 주 월요일 = 첫 번째 월요일 + 14일
        R = j + M + 14

    return R


def calc_special_day(c_year: int):
    """
    VBA의 CalcSpecialDay Sub를 1:1 변환.
    지정된 연도의 모든 기념일, 잡절, 24절기의 JD를 계산하여 SDay 전역 배열에 저장합니다.
    """
    global SDay

    i = 0
    E = julianday(float(c_year), 12.0, 31.0, 12.0, 0.0)  # Year End JD (Noon)
    S = julianday(float(c_year), 1.0, 1.0, 12.0, 0.0)  # Year Start JD (Noon)

    clear_s_day()
    read_day_data()

    # 1. 고정 기념일 계산 (Fixed Days)
    while SDay[i].M > 0 and i < 150:
        s_day = SDay[i]
        a = False

        if s_day.LuniSolar:
            # Lunar Day
            if s_day.y > -10000:
                # Year-specific Lunar Day
                # Placeholder: Use actual FindTBLInv
                a = find_tbl_inv(s_day.y, s_day.M, s_day.D, s_day.LeapMonth, s_day.RealDay)
                # Since RealDay is not passed by ref, we assume it's set globally or via return (not possible here)
                # We need to adapt the logic assuming find_tbl_inv returns RealDay or use another method.
                # *** Dummy implementation: assumes RealDay is set by external call if 'a' is True ***

                # If FindTBLInv is successful, 'a' is True and s_day.RealDay is set.
                # If 'a' is False, the month/day combination doesn't exist for the year.

            elif s_day.y <= -10000 and s_day.y > -15000:
                # Floating Lunar Day (apply to cYear)
                # Placeholder: Need a function to convert Lunar M/D (cYear) to Solar JD
                # For simplicity, we skip precise floating Lunar day calculation here,
                # as it requires heavy external functions.
                # We assume the external lunar-to-solar function is called elsewhere or
                # that these lunar days are handled in FindSDayL (below).
                a = True
                s_day.RealDay = 1.0  # Placeholder value to prevent M = -1
        else:
            # Solar Day
            if s_day.y > -10000:
                # Year-specific Solar Day (e.g., Christmas 2024)
                s_day.RealDay = julianday(float(s_day.y), float(s_day.M), float(s_day.D), 12.0, 0.0)
            elif s_day.y <= -10000 and s_day.y > -15000:
                # Floating Solar Day (apply to cYear)
                s_day.RealDay = julianday(float(c_year), float(s_day.M), float(s_day.D), 12.0, 0.0)

        # Skip days that don't exist (only applicable if 'a' logic was complete)
        # if not a:
        #     s_day.M = -1

        i += 1

    # 2. 잡절 더하기 (Other Variable Days: HANSHEK, SAMBOK, EASTER, etc.)
    N = i
    for day_kind in range(8):
        s_day = SDay[N]
        s_day.RealDay = get_other_day(day_kind, c_year)

        # Check if the calculated JD falls outside the target year [S, E]
        # If outside, try adjacent years to capture days near the boundary (e.g., late Dec or early Jan)
        if s_day.RealDay > E:
            s_day.RealDay = get_other_day(day_kind, c_year - 1)
        elif s_day.RealDay < S:
            s_day.RealDay = get_other_day(day_kind, c_year + 1)

        case_map = {
            0: ("한식", 0), 1: ("초복", 0), 2: ("중복", 0), 3: ("말복", 0),
            4: ("납향", 0), 5: ("제석", 1), 6: ("부활절", 0), 7: ("성년의 날", 0)
        }

        if day_kind in case_map:
            s_day.DayName, s_day.Holy = case_map[day_kind]
            s_day.M = 0  # Mark as processed ( 잡절)

        N += 1

    # 3. 24절기 더하기 (24 Solar Terms)
    jeolgi_names = "소한대한입춘우수경칩춘분청명곡우입하소만망종하지소서대서입추처서백로추분한로상강입동소설대설동지"

    for i in range(24):
        s_day = SDay[N]

        # Mid$(M, 1 + 2 * i, 2) -> Get 2-char name
        s_day.DayName = jeolgi_names[2 * i: 2 * i + 2]
        s_day.Holy = 0
        s_day.M = 0  # Mark as processed (절기)

        # Longitude for solar term: 285 + i * 15 (start=285 for 소한, end=270 for 동지)
        longitude = rev(285.0 + i * 15.0)

        s_day.RealDay = get_jd0(c_junggi(float(c_year), longitude, 5.0 + i * 15.0, TimeZone)) + 0.5

        # Boundary check, similar to 잡절
        if s_day.RealDay > E:
            s_day.RealDay = get_jd0(c_junggi(float(c_year - 1), longitude, 5.0 + i * 15.0, TimeZone)) + 0.5
        elif s_day.RealDay < S:
            s_day.RealDay = get_jd0(c_junggi(float(c_year + 1), longitude, 5.0 + i * 15.0, TimeZone)) + 0.5

        N += 1

    # 4. 상대 날짜 처리 (Relative Days: SDay(X).RealDay + g)
    for i in range(N):
        s_day = SDay[i]
        if s_day.y == -15000:
            # -15000: 상대 날짜 (Relative Day)
            # M = Index + 2, D = Days Offset
            X = s_day.M
            g = float(s_day.D)

            # X must be an index to a previously calculated day (X-2 is the correct index)
            if X > 2:
                # SDay(X-2).RealDay: 기준일 (Base Day)
                s_day.RealDay = get_jd0(SDay[X - 2].RealDay + g) + 0.5
            else:
                s_day.M = -1  # Invalid relative day


def find_s_day(jd: float) -> tuple[str, int]:
    """
    VBA의 FindSDay Function을 1:1 변환.
    주어진 JD에 해당하는 양력 기념일을 찾아 이름과 Holy 값을 반환합니다.
    (Holy value is returned by reference in VBA, simulated by tuple return here)
    """
    R = ""
    k = 0  # Holy value
    i = 0

    while SDay[i].M > -5 and i <= 200:
        s_day = SDay[i]

        # Check if JD matches the RealDay AND (it's a solar day OR it's a fixed lunar day)
        if (s_day.M > -1 and jd == s_day.RealDay) and \
                (not s_day.LuniSolar or s_day.y > -10000):

            if R != "" and s_day.DayName != "":
                R += ", "
            R += s_day.DayName

            # Holy Value Logic (Prioritization: 3 > 2/1 > 0)
            if (k == 1 and s_day.Holy == 2) or (k == 2 and s_day.Holy == 1):
                k = 3
            elif k == 3:
                k = 3
            elif k > 0 and s_day.Holy == 0:
                pass  # k remains the higher value
            else:
                k = s_day.Holy

        i += 1

    # h = k (VBA ByRef simulation)
    return R, k


def find_s_day_l(str_val: str, lm: int, ld: int, leap: bool, h_in: int) -> tuple[str, int]:
    """
    VBA의 FindSDayL Function을 1:1 변환.
    주어진 음력 월/일/윤달에 해당하는 음력 기념일(고정 연도가 아닌)을 찾아 추가합니다.
    """
    R = str_val
    k = h_in
    i = 0

    while SDay[i].M > -5 and i <= 200:
        s_day = SDay[i]

        # 1. Must be Lunar Day
        if s_day.LuniSolar and leap == s_day.LeapMonth:
            # 2. Must be a Floating Lunar Day (y <= -10000 and y > -15000)
            if s_day.M > -1 and s_day.y <= -10000 and s_day.y > -15000:
                # 3. Match Month and Day
                if lm == s_day.M and ld == s_day.D:
                    if R != "" and s_day.DayName != "":
                        R += ", "
                    R += s_day.DayName

                    # Holy Value Logic (same as FindSDay)
                    if (k == 1 and s_day.Holy == 2) or (k == 2 and s_day.Holy == 1):
                        k = 3
                    elif k == 3:
                        k = 3
                    elif k > 0 and s_day.Holy == 0:
                        pass
                    else:
                        k = s_day.Holy

        i += 1

    # h = k (VBA ByRef simulation)
    return R, k


def find_s_day_a(str_val: str, jd: float, tzz: float) -> str:
    """
    VBA의 FindSDayA Function을 1:1 변환.
    정확한 시간 정보(천체 현상 등)를 가진 기념일을 찾아 시간 정보를 추가하여 반환합니다.

    Note: Requires E and S arrays to be globally defined, which are missing here.
    Assuming E (Julian Day array) and S (Event Name array) are available globally.
    """
    R = str_val
    i = 0

    # Placeholder for E (Event JD) and S (Event Name)
    # The VBA code seems to rely on externally calculated, time-specific events (e.g., eclipses).
    E: List[float] = []
    S_names: List[str] = []

    if not E:  # Check if list E is empty (placeholder safety)
        return R

    while i < len(E):
        event_jd_at_tz = E[i] + tzz / 24.0

        # Check if the event JD (adjusted for TZ) rounds to the target JD.5
        if jd == get_jd0(event_jd_at_tz) + 0.5:
            if R != "" and S_names[i] != "":
                R += ", "

            # Combine event name with formatted time string
            R += S_names[i] + make_time_string(event_jd_at_tz)

        i += 1

    return R
