"""
Project: KASI.Lunar - 한국천문연구원 데이터를 기반으로 한 음/양력 변환 클래스
Files: Lunar.py
Dependency:
  - calendar module

이 패키지는 한국천문연구원의 음양력 데이터를 기반으로 하여 양력/음열간의 변환을
제공하며, aero님의 Date-Korean-0.0.2 perl module을 PHP에서 Python으로 포팅한 것이다.

양력 기준으로 1391-02-05 부터 2050-12-31 까지의 기간만 가능하며, 절기, 합삭/망
정보, 세차/월간/일진등의 정보는 별도로 처리해야 한다.

@category    Calendar
@package     KASI.Lunar
@author      JoungKyun.Kim <http://oops.org>
@copyright   (c) 2024, OOPS.org
@license     GPL (or Perl license)
@link        https://github.com/OOPS-ORG-PHP/KASI-Lunar
"""

import re
import time
from datetime import datetime, timezone
from calendar import weekday
import calendar


class Lunar:
    """
    한국천문연구원 데이터를 기반으로 한 음/양력 변환 클래스

    이 패키지는 한국천문연구원의 음양력 데이터를 기반으로 하여 양력/음열간의 변환을
    제공하며, aero님의 Date-Korean-0.0.2 perl module을 PHP로 포팅한 것이다.

    양력 기준으로 1391-02-05 부터 2050-12-31 까지의 기간만 가능하며, 절기, 합삭/망
    정보, 세차/월간/일진등의 정보는 별도로 처리해야 한다.

    @package     KASI.Lunar
    @author      JoungKyun.Kim <http://oops.org>
    @copyright   (c) 2024, OOPS.org
    @license     GPL (or Perl license)
    """

    # +-- public properties
    def __init__(self):
        """
        생성자
        """
        self.is_exception = True  # enable exception

    # +-- public version (void)
    def version(self):
        """
        KASI_Lunar 의 현재 버전을 출력

        @access public
        @return string  KASI_Lunar 버전
        """
        # 관리를 위해 꼭 single quote 를 사용한다!
        return '2.0.1'

    # +-- private (array) toargs ($v, $lanur = False)
    def toargs(self, v, lunar=False):
        """
        입력된 날자 형식을 연/월/일의 멤버를 가지는 배열로 반환한다.
        입력된 변수 값은 YYYY-MM-DD 형식으로 변환 된다.

        @access private
        @return list
        [
            2013,
            7,
            16
        ]
        @param v: string|int 날자형식
          - unixstmap (1970년 12월 15일 이후부터 가능)
          - Ymd or Y-m-d
          - None data (현재 시간)
        """
        if v is None:
            now = datetime.now()
            y = now.year
            m = now.month
            d = now.day
        else:
            if lunar:
                pass

            if isinstance(v, (int, float)) and v > 30000000:
                # unit stamp ?
                dt = datetime.fromtimestamp(v)
                y = dt.year
                m = dt.month
                d = dt.day
            else:
                match = re.match(r'^(-?[0-9]{1,4})[\/-]?([0-9]{1,2})[\/-]?([0-9]{1,2})$', str(v).strip())
                if match:
                    y, m, d = match.groups()
                    y, m, d = int(y), int(m), int(d)
                else:
                    if self.is_exception:
                        raise LunarException('Invalid Date Format')
                    return False

            if not lunar and y > 1969 and y < 2038:
                try:
                    fixed = datetime(y, m, d)
                    y = fixed.year
                    m = fixed.month
                    d = fixed.day
                except ValueError:
                    if self.is_exception:
                        raise LunarException('Invalid Date Format')
                    return False
            else:
                if m > 12 or d > 31:
                    if self.is_exception:
                        raise LunarException('Invalid Date Format')
                    return False

        # v 값을 문자열로 업데이트 (참조 전달 효과)
        # Python에서는 immutable 타입이므로 반환값으로 처리
        return [y, m, d]

    # +-- public (object) tolunar ($v = None)
    def tolunar(self, v=None):
        """
        양력 날자를 음력으로 변환

        @access public
        @return dict    음력 날자 정보 반환

        dict {
            'fmt': '2013-06-09',       # YYYY-MM-DD 형식의 음력 날자
            'jd': 2456582,             # 율리어스 적일
            'year': 2013,              # 연도
            'month': 6,                # 월
            'day': 9,                  # 일
            'week': 0,                 # 요일
            'leap': False,             # 음력 윤달 여부
            'lmoon': True              # 평달/큰달 여부
        }

        @param v: int|string   날자형식
          - unixstmap (1970년 12월 15일 이후부터 가능)
          - Ymd or Y-m-d
          - None data (현재 시간)
          - 1582년 10월 15일 이전의 날자는 율리우스력의 날자로 취급함.
            예.. 10월 14일은 그레고리력 10월 24일
        """
        y, m, d = self.toargs(v)

        jd = self.cal2jd([y, m, d])

        if jd < Tables.MinDate or jd > Tables.MaxDate:
            if self.is_exception:
                raise LunarException(
                    'Invalid date period. Valid period is from 1391-02-05 to 2050-12-31 with solar'
                )
            return False

        day = jd - Tables.MinDate

        mon = self.bisect(Tables.month, day)
        yer = self.bisect(Tables.year, mon)

        month = mon - Tables.year[yer] + 1
        days = day - Tables.month[mon] + 1

        # 큰달 작은달 체크
        lmoon = Tables.month[mon + 1] - Tables.month[mon]
        lmoon = False if lmoon == 29 else True

        # 윤달 체크
        leap = False
        if Tables.leap[yer] != 0 and Tables.leap[yer] <= month:
            if Tables.leap[yer] == month:
                leap = True
            month -= 1

        year = yer + Tables.BaseYear

        return {
            'fmt': self.datestring(year, month, days, '-'),
            'jd': jd,
            'year': year,
            'month': month,
            'day': days,
            'week': self.jd2week(jd),
            'leap': leap,
            'lmoon': lmoon
        }

    # +-- public (object) tosolar ($v = None, $leap = False)
    def tosolar(self, v=None, leap=False):
        """
        음력 날자를 양력으로 변환.

        @access public
        @return dict    양력 날자 정보 dict 반환

        dict {
            'fmt': '2013-06-09',       # YYYY-MM-DD 형식의 음력 날자
            'jd': 2456527,             # 율리어스 적일
            'year': 2013,              # 양력 연도
            'month': 7,                # 월
            'day': 16,                 # 일
            'week': 6                  # 요일
        }

        @param v: int|string 날자형식
          - unixstmap (1970년 12월 15일 이후부터 가능)
          - Ymd or Y-m-d
          - None data (현재 시간)

        @param leap: bool 윤달여부
        """
        y, m, d = self.toargs(v, True)

        yer = y - Tables.BaseYear

        # 윤달이 아닐 경우 값 보정
        if leap and (Tables.leap[yer] - 1) != m:
            leap = False

        month = Tables.year[yer] + m - 1

        if leap and (m + 1) == Tables.leap[yer]:
            month += 1
        elif Tables.leap[yer] and Tables.leap[yer] <= m:
            month += 1

        day = Tables.month[month] + d - 1
        if d < 1 or day >= Tables.month[month + 1]:
            raise LunarException('Invalid day')

        day += Tables.MinDate
        r = self.jd2cal(day)

        return {
            'fmt': self.datestring(r['year'], r['month'], r['day'], '-'),
            'jd': day,
            'year': r['year'],
            'month': r['month'],
            'day': r['day'],
            'week': r['week']
        }

    # +-- public (int) cal2jd ($v)
    def cal2jd(self, v):
        """
        날자를 율리우스 적일로 변환

        @access public
        @return int 율리우스 적일(integer)
        @param v: array 연/월/일 배열 : [y, m, d]
        """
        y, m, d = v

        julian = False

        datestr = self.datestring(y, m, d)
        julian = False
        if int(datestr) < 15821015:
            julian = True
            if int(datestr) > 15821004:
                d += 10
                julian = False

        if julian:
            # 율리우스력을 율리우스 적일로 변환
            a = (14 - m) // 12
            y_adj = y + 4800 - a
            m_adj = m + 12 * a - 3
            jd = d + (153 * m_adj + 2) // 5 + 365 * y_adj + y_adj // 4 - 32083
        else:
            # 그레고리력을 율리우스 적일로 변환
            if y < 1:
                y -= 1
            a = (14 - m) // 12
            y_adj = y + 4800 - a
            m_adj = m + 12 * a - 3
            jd = d + (153 * m_adj + 2) // 5 + 365 * y_adj + y_adj // 4 - y_adj // 100 + y_adj // 400 - 32045

        return jd

    # +-- public (object) cal4jd ($jd = None)
    def cal4jd(self, jd=None):
        """
        율리우스 적일을 율리우스력 또는 그레고리력으로 변환

        KASI.Lunar.jd2cal 의 alias method로 deprecated
        되었기 때문에 jd2cal method로 변경 해야 함.

        1.0.2 부터 삭제 예정

        @access public
        @return dict    율리우스력 또는 그레고리력 정보

        dict {
            'year': 2013,              # 양력 연도
            'month': 7,                # 월
            'day': 16,                 # 일
            'week': 6                  # 요일
        }

        @param jd: int 율리우스 적일. [default: 현재날의 적일]
        @deprecated deprecated since version 1.0.1
        """
        return self.jd2cal(jd)

    # +-- public (object) jd2cal ($jd = None)
    def jd2cal(self, jd=None):
        """
        율리우스 적일을 율리우스력 또는 그레고리력으로 변환

        @access public
        @return dict    율리우스력 또는 그레고리력 정보

        dict {
            'year': 2013,              # 양력 연도
            'month': 7,                # 월
            'day': 16,                 # 일
            'week': 6                  # 요일
        }

        @param jd: int 율리우스 적일. [default: 현재날의 적일]
        """
        if jd is None:
            # 현재 시간의 율리우스 적일 계산
            now = datetime.now()
            jd = self.cal2jd([now.year, now.month, now.day])

        # 그레고리력과 율리우스력 구분
        gregorian = jd > 2299160

        if gregorian:
            # 그레고리력 변환
            a = jd + 32044
            b = (4 * a + 3) // 146097
            c = a - (146097 * b) // 4
            d = (4 * c + 3) // 1461
            e = c - (1461 * d) // 4
            m = (5 * e + 2) // 153

            day = e - (153 * m + 2) // 5 + 1
            month = m + 3 - 12 * (m // 10)
            year = 100 * b + d - 4800 + m // 10
        else:
            # 율리우스력 변환
            b = 0
            c = jd + 32082
            d = (4 * c + 3) // 1461
            e = c - (1461 * d) // 4
            m = (5 * e + 2) // 153

            day = e - (153 * m + 2) // 5 + 1
            month = m + 3 - 12 * (m // 10)
            year = d - 4800 + m // 10

        if year < 0:
            year += 1

        # 요일 계산
        week = int((jd + 1) % 7)

        return {
            'year': int(year),
            'month': int(month),
            'day': int(day),
            'week': week
        }

    # +-- public (int) jd2week ($jd = None)
    def jd2week(self, jd=None):
        """
        율리우스 적일로 요일 정보를 구함

        @access public
        @return int         요일 배열 인덱스

        0(일) ~ 6(토)

        @param jd: int 율리우스 적일. [default: 현재날의 적일]
        """
        if jd is None:
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')
            t = today.split('-')
            jd = self.cal2jd(t)

        return int((jd + 1) % 7)

    # +-- public (object) season ($so, $year = None)
    def season(self, name, year=None):
        """
        연도별 절기의 입절시각을 구함

        @access public
        @return dict|False

        dict {
            'name': '입춘',            # 절기 이름
            'hname': '立春',           # 절기 한지 이름
            'stamp': 1073348340,       # 입절시각. Unix timestamp
            'date': '2004-02-04 20:56',# 입절 시각. YYYY-MM-DD HH:mm 형식의 양력 날자
            'year': 2004,              # 입절 시각 연도
            'month': 2,                # 입절 시각 월
            'day': 4,                  # 입절 시각 일
            'hour': 20,                # 입절 시각 시간
            'min': 56                  # 입절 시각 분
        }

        @param year: int 연도
        @param name: string 절기 이름
        """
        if year is None:
            year = datetime.now().year

        if year > 2026 or year < 2004:
            if self.is_exception:
                raise LunarException('Support between 2004 and 2026')
            return False

        try:
            id = Seasons.so24n.index(name)
        except ValueError:
            if self.is_exception:
                raise LunarException(f"Invalid Invalid season name ({name}).")
            return False

        hid = Seasons.so24hn[id]
        # 절기 배열은 2004년이 첫번째 배열이다.
        sid = year - 2004
        so = Seasons.so24[sid][id]

        t = datetime.fromtimestamp(so).strftime('%Y-%m-%d-%H-%M-%S').split('-')

        return {
            'name': name,
            'hname': hid,
            'stamp': so,
            'date': f"{t[0]}-{t[1]}-{t[2]} {t[3]}:{t[4]}",
            'year': int(t[0]),
            'month': int(t[1]),
            'day': int(t[2]),
            'hour': int(t[3]),
            'min': int(t[4])
        }

    # +-- private bisect ($a, $x)
    def bisect(self, a, x):
        """이진 탐색"""
        lo = 0
        hi = len(a)

        while lo < hi:
            mid = (lo + hi) // 2
            if x < a[mid]:
                hi = mid
            else:
                lo = mid + 1

        return lo - 1

    # +-- private datestring ($y, $m, $d)
    def datestring(self, y, m, d, dash=''):
        """날짜 문자열 생성"""
        if m < 10:
            m = '0' + str(int(m))
        else:
            m = str(m)

        if d < 10:
            d = '0' + str(int(d))
        else:
            d = str(d)

        return str(y) + dash + m + dash + d


def main():
    lunar = Lunar
    print(lunar.tosolar('1972-01-03'))


if __name__ == '__main__':
    main()
