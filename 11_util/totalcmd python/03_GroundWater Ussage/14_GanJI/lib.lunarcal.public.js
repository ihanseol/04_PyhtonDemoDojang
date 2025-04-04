/**************************************************
 * 양음력 계산 라이브러리 -- Library file for Korean Lunar Calendar
 * by Senarin
 **************************************************/
var DAY0000 = 1721424.5; // 0000/12/31
var SOLAR_EPOCH = 1721425.5; // 0001/1/1
var YEAR_MIN = 1583; // Min. Year
var YEAR_MAX = 2100; // Max. Year
var LUNAR_EPOCH = 2299261.5;
var LOWER_LIMIT = LUNAR_EPOCH;
var UPPER_LIMIT = 2488461.5;

var daysPerMonth = new Array(31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31); // Days of the Month
var kstems = new Array("갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"); // 십간 (한글) - Stems (Korean)
var hstems = new Array("甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"); // 십간 (한자) - Stems (Hanja)

var kbranches = new Array("자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"); // 십이지 (한글) - Branches (Korean)
var hbranches = new Array("子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"); // 십이지 (한자) - Branches (Hanja)

var kowkdays = new Array("일", "월", "화", "수", "목", "금", "토"); // 한국어 요일명 - Weekdays (Korean)
var enwkdays = new Array("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"); // 영문 요일명 - Weekdays (English)


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

// 1583년 ~ 2100년까지의 자료.
var lunarMonthTab = new Array(
    [1, 5, 1, 2, 1, 1, 2, 1, 2, 2, 2, 2],  /* 1583 */
    [1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2],
    [1, 2, 2, 1, 1, 2, 1, 1, 5, 2, 2, 1],  /* 1585 */
    [2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 4, 2, 1, 2, 1, 1, 2],
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2],
    [1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 4, 1, 1, 2, 1, 2, 2, 2, 2, 1],  /* 1591 */
    [2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1],
    [2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 5, 2],
    [2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1],  /* 1595 */
    [2, 2, 1, 2, 2, 1, 2, 3, 2, 1, 2, 1],
    [2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 2],
    [1, 1, 2, 3, 2, 2, 1, 2, 2, 1, 2, 2],
    [1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2],  /* 1600 */
    [2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2],  /* 1601 */ // 0
    [2, 5, 1, 2, 1, 1, 2, 2, 1, 1, 2, 2],
    [2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 2, 1, 2, 1, 1, 5, 2, 1, 2],
    [1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],  /* 1605 */
    [2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 5, 2, 2, 1, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2, 2],
    [1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2],
    [1, 2, 4, 1, 1, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2],  /* 1611 */ // 10
    [2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 4, 1],
    [2, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 2, 1, 5, 2, 1, 2, 1],
    [2, 1, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 2, 3, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 2],
    [1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1],
    [2, 6, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1],  /* 1621 */ //20
    [2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 2, 1, 2, 1, 2, 4, 1, 2],
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1],
    [2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 4, 1, 2, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 2, 1],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2],
    [2, 2, 1, 5, 1, 2, 1, 1, 2, 2, 1, 2],
    [2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2],
    [2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 5, 2],  /* 1631 */ //30
    [2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1],
    [2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 1],
    [2, 1, 1, 2, 1, 2, 1, 6, 2, 1, 2, 1],
    [2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2],
    [1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2],
    [2, 1, 2, 3, 2, 1, 1, 2, 1, 2, 2, 2],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2],
    [5, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1],  /* 1641 */ //40
    [2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 5, 2],
    [1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2],
    [1, 2, 1, 1, 2, 3, 2, 1, 2, 2, 2, 2],
    [1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2],
    [1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2],
    [1, 2, 5, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 3, 2],
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2],  /* 1651 */ //50
    [1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1],
    [2, 1, 1, 2, 1, 1, 5, 2, 2, 2, 2, 1],
    [2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1],
    [2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1],
    [2, 2, 1, 2, 4, 1, 1, 2, 1, 2, 1, 2],
    [2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2],
    [1, 2, 4, 2, 1, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 1, 2, 5, 2, 2, 1, 2, 1],  /* 1661 */ //60
    [2, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2],
    [2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2],
    [2, 1, 2, 1, 2, 3, 2, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 1, 2, 5, 2, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1],
    [2, 4, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1],
    [2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2],  /* 1671 */ //70
    [1, 2, 1, 2, 1, 1, 5, 2, 1, 2, 2, 2],
    [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2],
    [1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2],
    [1, 2, 2, 2, 4, 1, 1, 2, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 2],
    [1, 2, 3, 2, 2, 1, 2, 2, 1, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 2, 1, 1, 2, 1, 5, 2, 2, 2, 1],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 1],  /* 1681 */ //80
    [2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1],
    [2, 2, 2, 1, 2, 3, 2, 1, 1, 2, 2, 1],
    [2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1],
    [2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 4, 1, 2, 2, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 5, 1, 2, 1, 1, 2, 2, 2, 1, 2],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2],
    [2, 2, 1, 2, 1, 1, 5, 1, 2, 1, 2, 2],  /* 1691 */ //90
    [2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2],
    [2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1],
    [2, 2, 1, 2, 4, 2, 1, 2, 1, 2, 1, 1],
    [2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2],
    [1, 2, 3, 2, 1, 2, 1, 2, 2, 1, 2, 2],
    [1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 1, 2],
    [2, 1, 2, 1, 1, 2, 3, 2, 1, 2, 2, 2],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2],  /* 1701 */ //100
    [2, 1, 2, 2, 1, 5, 2, 1, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1],
    [2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1],
    [1, 2, 1, 5, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2],
    [1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2],
    [1, 2, 5, 1, 2, 1, 1, 2, 1, 2, 2, 2],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2],
    [1, 2, 2, 1, 2, 1, 5, 1, 2, 1, 2, 1],
    [2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2],  /* 1711 */ //110
    [1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 5, 2, 2, 1, 2, 2, 1, 1],
    [2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1],
    [2, 2, 3, 2, 1, 1, 2, 1, 2, 2, 2, 1],
    [2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1],
    [2, 2, 1, 2, 1, 2, 1, 4, 1, 2, 1, 2],
    [2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 2, 4, 1, 2, 1, 2, 1, 2],  /* 1721*/ //120
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 2],
    [1, 2, 1, 5, 1, 2, 1, 2, 2, 2, 1, 2],
    [1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2],
    [2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 2, 5, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 1, 2, 2, 1, 2, 4, 1, 2, 1, 2, 1],
    [2, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1],  /* 1731 */ // 130
    [2, 1, 2, 1, 4, 1, 2, 2, 2, 1, 2, 1],
    [2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2],
    [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2],
    [2, 1, 2, 4, 1, 1, 1, 2, 1, 2, 2, 2],
    [1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2],
    [1, 2, 2, 1, 2, 1, 2, 1, 5, 1, 2, 2],
    [1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2],
    [1, 2, 1, 1, 2, 5, 2, 2, 1, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1],  /* 1741 */ //140
    [2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 1, 5, 1, 1, 2, 1, 2, 2, 2, 1],
    [2, 2, 1, 2, 1, 1, 1, 2, 1, 2, 2, 1],
    [2, 2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2],
    [1, 2, 5, 2, 1, 2, 1, 2, 1, 1, 2, 1],
    [2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 2, 1, 6, 1, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 2, 1, 4, 1, 1, 2, 2, 1, 2, 2],  /* 1751 */ //150
    [2, 1, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2],
    [2, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2],
    [2, 2, 1, 5, 2, 1, 2, 1, 1, 2, 1, 2],
    [2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1],
    [2, 2, 1, 2, 1, 2, 2, 1, 5, 1, 2, 1],
    [2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2],
    [1, 1, 2, 1, 2, 4, 1, 2, 2, 1, 2, 2],
    [1, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2, 2],
    [2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2],  /* 1761 */ //160
    [2, 1, 2, 2, 3, 1, 2, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1],
    [2, 4, 2, 1, 2, 1, 2, 2, 1, 1, 2, 1],
    [2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1],
    [1, 2, 1, 2, 1, 2, 4, 2, 1, 2, 2, 1],
    [1, 2, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2],
    [1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 2, 1, 3, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2],  /* 1771 */ //170
    [1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [1, 2, 5, 2, 2, 1, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 1, 2, 2, 1, 5, 2, 1],
    [2, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 1, 2, 1, 5, 2, 1, 2, 2, 2, 1],
    [2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1],
    [2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1],
    [2, 2, 2, 1, 5, 1, 2, 1, 2, 1, 2, 1],  /* 1781 */ //180
    [2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 5, 2, 1, 2, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 5, 2, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2],
    [2, 2, 1, 2, 3, 2, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2],  /* 1791 */ //190
    [1, 2, 1, 5, 2, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 2, 1],
    [2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2],
    [1, 5, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2],
    [2, 1, 2, 1, 2, 3, 1, 2, 1, 2, 2, 2],
    [1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2],
    [1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2],
    [2, 1, 2, 5, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2],  /* 1801 */ //200
    [1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1],
    [2, 3, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2],
    [1, 2, 1, 2, 1, 3, 2, 1, 2, 2, 2, 1],
    [2, 2, 1, 2, 1, 1, 1, 2, 1, 2, 2, 1],
    [2, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2],
    [1, 2, 2, 1, 5, 2, 1, 2, 1, 1, 2, 1],
    [2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2],
    [1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2],
    [1, 1, 5, 2, 1, 2, 2, 1, 2, 2, 1, 2],  /* 1811 */ //210
    [1, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1],
    [2, 5, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2],
    [2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 2, 1, 2, 1, 5, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1],
    [2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 1, 2],
    [1, 2, 1, 5, 2, 2, 1, 2, 2, 1, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2],
    [1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2],  /* 1821 */ //220
    [2, 1, 5, 1, 1, 2, 1, 2, 2, 1, 2, 2],
    [2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 2, 1, 4, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 1, 2, 2, 4, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2],
    [1, 1, 2, 3, 2, 1, 2, 2, 1, 2, 2, 2],
    [1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2],  /* 1831 */ //230
    [1, 2, 1, 2, 1, 1, 2, 1, 5, 2, 2, 2],
    [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2],
    [1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 5, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2],
    [1, 2, 1, 5, 1, 2, 2, 1, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 4, 1, 1, 2, 1, 2, 1, 2, 2, 1],   /* 1841 */ //240
    [2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1],
    [2, 2, 2, 1, 2, 1, 4, 1, 2, 1, 2, 1],
    [2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 5, 2, 1, 2, 2, 1, 2, 1],
    [2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 2, 3, 2, 1, 2, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2],
    [2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 5, 2],   /* 1851 */ // 250
    [2, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2],
    [2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 5, 2, 1, 2, 1, 2],
    [1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1],
    [2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2],
    [1, 2, 1, 1, 5, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2],
    [2, 1, 6, 1, 1, 2, 1, 1, 2, 1, 2, 2],
    [1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2],   /* 1861 */
    [2, 1, 2, 1, 2, 2, 1, 2, 2, 3, 1, 2],
    [1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2],
    [1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 1, 2, 4, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2],
    [1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2],
    [1, 2, 2, 3, 2, 1, 1, 2, 1, 2, 2, 1],
    [2, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 2, 2, 1, 2, 1, 2, 1, 1, 5, 2, 1],
    [2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2],   /* 1871 */
    [1, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2],
    [1, 1, 2, 1, 2, 4, 2, 1, 2, 2, 1, 2],
    [1, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1],
    [2, 2, 1, 1, 5, 1, 2, 1, 2, 2, 1, 2],
    [2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 2, 4, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 1, 2],
    [1, 2, 1, 2, 1, 2, 5, 2, 2, 1, 2, 1],   /* 1881 */
    [1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2],
    [1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2],
    [2, 1, 1, 2, 3, 2, 1, 2, 2, 1, 2, 2],
    [2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 2, 1, 5, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2],
    [1, 5, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2],   /* 1891 */
    [1, 1, 2, 1, 1, 5, 2, 2, 1, 2, 2, 2],
    [1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 5, 1, 2, 1, 2, 1, 2, 1],
    [2, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 5, 2, 2, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 5, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1],   /* 1901 */
    [2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 1, 2, 3, 2, 1, 1, 2, 2, 1, 2],
    [2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1],
    [2, 2, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2],
    [1, 2, 2, 4, 1, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1],
    [2, 1, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2],
    [1, 5, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 2, 1, 1, 5, 1, 2, 2, 1, 2, 2],   /* 1911 */
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2],
    [2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2],
    [2, 2, 1, 2, 5, 1, 2, 1, 2, 1, 1, 2],
    [2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1],
    [2, 3, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1],
    [2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 5, 2, 2, 1, 2, 2],
    [1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2],   /* 1921 */
    [2, 1, 2, 2, 3, 2, 1, 1, 2, 1, 2, 2],
    [1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2],
    [2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1],
    [2, 1, 2, 5, 2, 1, 2, 2, 1, 2, 1, 2],
    [1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2],
    [1, 5, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2],
    [1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2],
    [1, 2, 2, 1, 1, 5, 1, 2, 1, 2, 2, 1],
    [2, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1],   /* 1931 */
    [2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2],
    [1, 2, 2, 1, 6, 1, 2, 1, 2, 1, 1, 2],
    [1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2],
    [1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 4, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1],
    [2, 2, 1, 1, 2, 1, 4, 1, 2, 2, 1, 2],
    [2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 2, 1, 2, 2, 4, 1, 1, 2, 1, 2, 1],   /* 1941 */
    [2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 1, 2],
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2],
    [1, 1, 2, 4, 1, 2, 1, 2, 2, 1, 2, 2],
    [1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2],
    [2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2],
    [2, 5, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 2, 1, 2, 1, 2, 3, 2, 1, 2, 1, 2],
    [2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2],   /* 1951 */
    [1, 2, 1, 2, 4, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 2, 2],
    [1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2],
    [2, 1, 4, 1, 1, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 2, 1, 1, 5, 2, 1, 2, 2],
    [1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 5, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2],   /* 1961 */
    [1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 2, 3, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1],
    [2, 2, 5, 2, 1, 1, 2, 1, 1, 2, 2, 1],
    [2, 2, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 1, 5, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1],
    [2, 1, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2],
    [1, 2, 1, 1, 5, 2, 1, 2, 2, 2, 1, 2],   /* 1971 */
    [1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 1],
    [2, 2, 1, 5, 1, 2, 1, 1, 2, 2, 1, 2],
    [2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2],
    [2, 2, 1, 2, 1, 2, 1, 5, 2, 1, 1, 2],
    [2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1],
    [2, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1],
    [2, 1, 1, 2, 1, 6, 1, 2, 2, 1, 2, 1],
    [2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2],
    [1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2],   /* 1981 */
    [2, 1, 2, 3, 2, 1, 1, 2, 2, 1, 2, 2],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2],
    [2, 1, 2, 2, 1, 1, 2, 1, 1, 5, 2, 2],
    [1, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1],
    [2, 1, 2, 2, 1, 5, 2, 2, 1, 2, 1, 2],
    [1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2],
    [1, 2, 1, 1, 5, 1, 2, 1, 2, 2, 2, 2],
    [1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2],   /* 1991 */
    [1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2],
    [1, 2, 5, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 2, 1, 5, 2, 1, 1, 2],
    [1, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2],
    [1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 1, 2, 3, 2, 2, 1, 2, 2, 2, 1],
    [2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1],
    [2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1],
    [2, 2, 2, 3, 2, 1, 1, 2, 1, 2, 1, 2],   /* 2001 */
    [2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2],
    [1, 5, 2, 2, 1, 2, 1, 2, 2, 1, 1, 2],
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1],
    [2, 1, 2, 1, 2, 1, 5, 2, 2, 1, 2, 2],
    [1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2],
    [2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2],
    [2, 2, 1, 1, 5, 1, 2, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1],   /* 2011 */
    [2, 1, 6, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 1, 2, 5, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2, 2],
    [1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2],
    [2, 1, 1, 2, 3, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 5, 2, 1, 1, 2, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],   /* 2021 */
    [2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2],
    [1, 5, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 2, 1, 1, 5, 2, 1, 2, 2, 2, 1],
    [2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2],
    [1, 2, 2, 1, 5, 1, 2, 1, 1, 2, 2, 1],
    [2, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2],
    [1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 5, 2, 1, 2, 2, 1, 2, 1, 2, 1],   /* 2031 */
    [2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 5, 2],  /* 2033 -- 윤달을 7월로 정할 것인가 11월로 정할 것인가에 대한 문제가 있음. 파일 윗부분 주석 내 URL 참고 */
    [1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2],
    [2, 2, 1, 2, 1, 4, 1, 1, 2, 1, 2, 2],
    [2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2],
    [2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1],
    [2, 2, 1, 2, 5, 2, 1, 2, 1, 2, 1, 1],
    [2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 1],
    [2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2],   /* 2041 */
    [1, 5, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2],   /* 2043 */
    [2, 1, 2, 1, 1, 2, 3, 2, 1, 2, 2, 2],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2],
    [2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2],
    [2, 1, 2, 2, 4, 1, 2, 1, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1],
    [2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1],
    [1, 2, 4, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2],  /* 2051 */
    [1, 2, 1, 1, 2, 1, 1, 5, 2, 2, 2, 2],
    [1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2],
    [1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2],
    [1, 2, 2, 1, 2, 4, 1, 1, 2, 1, 2, 1],
    [2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2],
    [1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 2, 1],
    [2, 1, 2, 4, 2, 1, 2, 1, 2, 2, 1, 1],
    [2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1],
    [2, 2, 3, 2, 1, 1, 2, 1, 2, 2, 2, 1],   /* 2061 */
    [2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1],
    [2, 2, 1, 2, 1, 2, 3, 2, 1, 2, 1, 2],
    [2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2],
    [1, 2, 1, 2, 5, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 2],
    [1, 2, 1, 5, 1, 2, 1, 2, 2, 2, 1, 2],
    [2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2],
    [2, 1, 2, 1, 2, 1, 1, 5, 2, 1, 2, 2],   /* 2071 */
    [2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2],
    [2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1],
    [2, 1, 2, 2, 1, 5, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1],
    [2, 1, 2, 3, 2, 1, 2, 2, 2, 1, 2, 1],
    [2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2],
    [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2],
    [2, 1, 5, 2, 1, 1, 2, 1, 2, 1, 2, 2],
    [1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2],   /* 2081 */
    [1, 2, 2, 2, 1, 2, 3, 2, 1, 1, 2, 2],
    [1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    [2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2],
    [1, 2, 1, 1, 6, 1, 2, 2, 1, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1],
    [2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2],
    [1, 2, 1, 5, 1, 2, 1, 1, 2, 2, 2, 1],
    [2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1],
    [2, 2, 2, 1, 2, 1, 1, 5, 1, 2, 2, 1],
    [2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1],   /* 2091 */
    [2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1],
    [1, 2, 2, 1, 2, 4, 2, 1, 2, 1, 2, 1],
    [2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2],
    [1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1],
    [2, 1, 2, 3, 2, 1, 1, 2, 2, 2, 1, 2],
    [2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2],
    [2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2],
    [2, 5, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2],
    [2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1]
);

// 양력 날짜를 율리우스 적일로 변환
function solar2JD(year, month, day) {
    if (month <= 2) {
        year--;
        month += 12;
    }
    var b;
    var checksum = (year * 10000) + (month * 100) + day;
    var a = Math.floor(year / 100);
    if (checksum >= 15821015) {
        b = 2 - a + Math.floor(a / 4);
    } else if (checksum <= 15821004) {
        b = 0;
    } else {
        return -1;
    }
    return Math.floor(365.25 * (year + 4716)) + Math.floor(30.6001 * (month + 1)) + day + (b - 1524.5);
}

// 율리우스 적일을 양력 날짜로 변환
function JD2solar(jd) {
    var numdays = Math.floor(jd + 0.5);
    var a;
    if (numdays < 2299161) {
        a = numdays;
    } else {
        var alpha = Math.floor((numdays - 1867216.25) / 36524.25);
        a = numdays + 1 + (alpha - Math.floor(alpha / 4));
    }
    var b = a + 1524;
    var c = Math.floor((b - 122.1) / 365.25);
    var d = Math.floor(c * 365.25);
    var e = Math.floor((b - d) / 30.6001);

    var month = (e < 14) ? (e - 1) : (e - 13);
    var year = (month > 2) ? (c - 4716) : (c - 4715);
    var day = b - d - Math.floor(30.6001 * e);
    return new Array(year, month, day);
}

// 양력을 음력으로 변환
function solar2lunar(year, month, day) {

    var m, mm, p, q;
    var i, j;
    var dt = new Array();
    var daysLunar;
    var absoluteDay1 = LUNAR_EPOCH - DAY0000;
    var edays = solar2JD(year, month, day);
    //var gyear=((edays > LOWER_LIMIT) && (edays < UPPER_LIMIT)) ? year : 0;
    var gyear = ((year >= YEAR_MIN) && (year <= YEAR_MAX)) ? year : 0;
    //document.write(gyear);
    if (gyear == 0) {
        return false;
    }
    daysPerMonth[1] = (leap_solar(gyear)) ? 29 : 28;
    var y = gyear - 1;
    var absoluteDay2 = solar2JD(year, month, day) - DAY0000;
    var absoluteDay = absoluteDay2 - absoluteDay1 + 1;
    for (i = 0; i <= gyear - 1583; i++) {
        dt[i] = 0;
        for (j = 0; j < 12; j++) {
            switch (lunarMonthTab[i][j]) {
                case 1:
                    daysLunar = 29;
                    break;
                case 2:
                    daysLunar = 30;
                    break;
                case 3:
                    daysLunar = 58; // 29+29
                    break;
                case 4:
                    daysLunar = 59; // 29+30
                    break;
                case 5:
                    daysLunar = 59; // 30+29
                    break;
                case 6:
                    daysLunar = 60; //30+30
                    break;
            }
            dt[i] += daysLunar;
        }
    }

    var p = 0;
    do {
        if (absoluteDay > dt[p]) {
            absoluteDay += -dt[p];
            p++;
        } else {
            break;
        }
    } while (true);
    var q = 0;
    var isLeap = 0;
    do {
        if (lunarMonthTab[p][q] <= 2) {
            m0 = lunarMonthTab[p][q] + 28;
            if (absoluteDay > m0) {
                absoluteDay += -m0;
                q++;
            } else {
                break;
            }
        } else {
            switch (lunarMonthTab[p][q]) {
                case 3:
                    var m1 = 29;
                    var m2 = 29;
                    break;
                case 4:
                    var m1 = 29;
                    var m2 = 30;
                    break;
                case 5:
                    var m1 = 30;
                    var m2 = 29;
                    break;
                case 6:
                    var m1 = 30;
                    var m2 = 30;
                    break;

            }

            if (absoluteDay > m1) {
                absoluteDay += -m1;
                if (absoluteDay > m2) {
                    absoluteDay += -m2;
                    q++;
                } else {
                    isLeap = 1;
                    break;
                }
            } else {
                break;
            }
        }
    } while (true);
    p += 1583;
    q++;
    var r = absoluteDay;
    var lyear = p;
    var lmonth = q;
    var lday = r;

    var nDays = solar2JD(year, month, day); // 양력 날짜에 해당하는 율리우스 적일
    var syear = (lyear + 6) % 10;
    var byear = (lyear - 4) % 12;
    var sbmonth = ((lyear * 12) + lmonth + 13) % 60;
    var smonth = sbmonth % 10;
    var bmonth = sbmonth % 12;
    var sday = Math.floor(nDays) % 10;
    var bday = (Math.floor(nDays) + 2) % 12;
    return new Array(lyear, lmonth, lday, isLeap, nDays, syear, byear, smonth, bmonth, sday, bday);
}


// 음력을 양력으로 변환
function lunar2solar(year, month, day, isLeap) {
    var lyear = ((year >= YEAR_MIN) && (year <= YEAR_MAX)) ? year : 0;
    if (lyear == 0) {
        return false;
    }
    var y = lyear - 1583;
    var m = month - 1;
    var mm;
    var y2;
    var yleap = 0;
    if (lunarMonthTab[y][m] > 2) {
        if (isLeap == 1) {
            yleap = 1;
            switch (lunarMonthTab[y][m]) {
                case 3:
                case 5:
                    mm = 29;
                    break;
                case 4:
                case 6:
                    mm = 30;
                    break;
            }
        } else {
            switch (lunarMonthTab[y][m]) {
                case 1:
                case 3:
                case 4:
                    mm = 29;
                case 2:
                case 5:
                case 6:
                    mm = 30;
            }
        }
    }
    lday = day;
    var absoluteDay = 0;
    for (i = 0; i < y; i++) {
        for (j = 0; j < 12; j++) {
            switch (lunarMonthTab[i][j]) {
                case 1:
                    absoluteDay += 29;
                    break;
                case 2:
                    absoluteDay += 30;
                    break;
                case 3:
                    absoluteDay += 58; // 29+29
                    break;
                case 4:
                    absoluteDay += 59; // 29+30
                    break;
                case 5:
                    absoluteDay += 59; // 30+29
                    break;
                case 6:
                    absoluteDay += 60; // 30+30
                    break;
            }
        }
    }
    for (j = 0; j < m; j++) {
        switch (lunarMonthTab[y][j]) {
            case 1:
                absoluteDay += 29;
                break;
            case 2:
                absoluteDay += 30;
                break;
            case 3:
                absoluteDay += 58; // 29+29
                break;
            case 4:
                absoluteDay += 59; // 29+30
                break;
            case 5:
                absoluteDay += 59; // 30+29
                break;
            case 6:
                absoluteDay += 60; // 30+30
                break;
        }
    }

    if (yleap == 1) {
        switch (lunarMonthTab[y][m]) {
            case 3:
            case 4:
                absoluteDay += 29;
                break;
            case 5:
            case 6:
                absoluteDay += 30;
                break;
        }
    }
    absoluteDay += lday + 33;
    y = 1582;
    do {
        y++;
        if (leap_solar(y)) {
            y2 = 366;
        } else {
            y2 = 365;
        }
        if (absoluteDay <= y2) {
            break;
        } else {
            absoluteDay += -y2;
        }
    } while (true);
    gyear = y;
    daysPerMonth[1] = y2 - 337;
    m = 0;
    do {
        m++;
        if (absoluteDay <= daysPerMonth[m - 1]) {
            break;
        } else {
            absoluteDay += -daysPerMonth[m - 1];
        }
    } while (true);
    var gmonth = m;
    var gday = absoluteDay;
    y = gyear - 1;
    var nDays = solar2JD(gyear, gmonth, gday); // 양력 날짜에 해당하는 율리우스 적일
    var syear = (year + 6) % 10;
    var byear = (year - 4) % 12;
    var sbmonth = ((year * 12) + month + 13) % 60;
    var smonth = sbmonth % 10;
    var bmonth = sbmonth % 12;
    var sday = Math.floor(nDays) % 10;
    var bday = (Math.floor(nDays) + 2) % 12;

    return new Array(gyear, gmonth, gday, yleap, nDays, syear, byear, smonth, bmonth, sday, bday);
}
