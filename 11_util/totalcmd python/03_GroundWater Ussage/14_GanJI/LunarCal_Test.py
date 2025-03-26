
# https://github.com/wolfhong/LunarCalendar/tree/master

# import datetime
# from lunarcalendar import Converter, Solar, Lunar, DateNotExist
# from lunarcalendar.festival import festivals
#
#
# solar = Solar(1972, 1, 3)
# print(solar)
# lunar = Converter.Solar2Lunar(solar)
# print(lunar)
# solar = Converter.Lunar2Solar(lunar)
# print(solar)
# print(solar.to_date(), type(solar.to_date()))
#
#
#
# # print festivals, using English or Chinese
# print("----- print all festivals on 2018 in chinese: -----")
# for fest in festivals:
#     print(fest.get_lang('en'), fest(2025))
#
#

from korean_lunar_calendar import KoreanLunarCalendar

calendar = KoreanLunarCalendar()

# params : year(년), month(월), day(일)
calendar.setSolarDate(1972, 1, 3)

# Lunar Date (ISO Format)
print(calendar.LunarIsoFormat())

# Korean GapJa String
print(calendar.getGapJaString())

# Chinese GapJa String
print(calendar.getChineseGapJaString())



print("-"*90)
calendar = KoreanLunarCalendar()

# params : year(년), month(월), day(일), intercalation(윤달여부)
calendar.setLunarDate(1971, 11, 17, False)

# Solar Date (ISO Format)
print(calendar.SolarIsoFormat())

# Korean GapJa String
print(calendar.getGapJaString())

# Chinese GapJa String
print(calendar.getChineseGapJaString())


