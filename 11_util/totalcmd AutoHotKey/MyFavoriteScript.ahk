;*******************************************************************************;
; Title:          My fav AHK scripts                                            ;
; Description:    AutoHotkey scripts that make my daily life a bit easier :)    ;
; Author:         How To Work From Home                                         ;
;*******************************************************************************;

; Keyboard shortcuts Matrix
; (hash)                #    Windows logo key
; (exclamation mark)    !    ALT
; (caret)               ^    CTRL
; (plus)                +    Shift


;******************************************************************************
;			Reload/Execute this script.ahk file
;******************************************************************************
;::rscript::

^!R::             ; CTRL + ALT + R
Reload , "c:\Program Files\totalcmd\ini\03_AutoHotKey\MyFavoriteScript.ahk"
Return


^e::exitapp

;******************************************************************************
;			Text replacements for most used keywords
;******************************************************************************

::]pr::Print('hello world)
Return

::]ty::Thank you,
Return

::]tyxx::Thank you,{enter}FirstName LastName
Return

::]yw::You're Welcome
Return

::]myph::123-456-7890
Return

::]mycell::098-765-4321
Return

::]ol::first.last@outlook.com
Return

::]hm::first.last@hotmail.com
Return

::]gm::first.last@gmail.com
Return

::]ym::first.last@yahoo.com
Return

::]myadd::
(
MINHWASOO
11, Gyeryong-ro 52beon-gil, Yuseong-gu,
Daejeon, Republic of Korea 604ho
604
Daejeon
Daejeon - 34178
)

;******************************************************************************
;			Computer information
;******************************************************************************
::]myid::
SendInput %A_UserName%
Return

::]myip::
SendInput %A_IPAddress1%
Return

::]mycomp::
SendInput %A_ComputerName%
Return


;******************************************************************************
;			Dash lines
;******************************************************************************
::]-10::----------
Return

::]-20::--------------------
Return

::]-30::------------------------------
Return

::]-40::----------------------------------------
Return

::]-50::--------------------------------------------------
Return

::]*10::**********
Return

::]*20::********************
Return

::]*30::******************************
Return

::]*40::****************************************
Return

::]*50::**************************************************
Return


;******************************************************************************
;			Microsoft Office AutoCorrect - Lowercase
;******************************************************************************
:C:abbout::about
:C:abotu::about
:C:abouta::about a
:C:aboutit::about it
:C:aboutthe::about the
:C:abscence::absence
:C:accesories::accessories
:C:accidant::accident
:C:accidantally::accidentally
:C:accomodate::accommodate
:C:accomodation::accommodation
:C:accordingto::according to
:C:accquire::acquire
:C:accross::across
:C:acheive::achieve
:C:acheived::achieved
:C:acheiving::achieving
:C:acn::can


;******************************************************************************
;			Microsoft Office AutoCorrect - Uppercase
;******************************************************************************
:C:Abbout::About
:C:Abotu::About
:C:Abouta::About a
:C:Aboutit::About it
:C:Aboutthe::About the
:C:Abscence::Absence
:C:Accesories::Accessories
:C:Accidant::Accident
:C:Accidantally::Accidentally
:C:Accomodate::Accommodate
:C:Accomodation::Accommodation
:C:Accordingto::According to
:C:Accquire::Acquire
:C:Accross::Across
:C:Acheive::Achieve
:C:Acheived::Achieved
:C:Acheiving::Achieving
:C:Acn::Can


;******************************************************************************
;			SQL Shortcuts
;******************************************************************************
::]sel*::SELECT`t*{enter}FROM`t{enter}WHERE`t1 = 1{enter}`tAND ROWNUM <= 10{enter}--`tAND Field_value_1 = upper('value'){enter}--`tAND upper(Field_value_2) LIKE upper('%value%');
Return


;******************************************************************************
;			Date/Time Stamps
;******************************************************************************

F1::
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
;SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

FormatTime, CurrentDateTime,, yyyy MMMM d, HH:mm:ss
KoreanDateTime := CurrentDateTime
RegExMatch(KoreanDateTime, "(\d+) (\d+)¿ù (\d+), (\d+):(\d+):(\d+)", Match)

; Convert month number to English name
MonthNames := ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
Month := MonthNames[Match2]

SendInput %CurrentDateTime%, %Month%
;~ SendInput %A_ScreenWidth%, %A_ScreenHeight%


return




::]d::
FormatTime, CurrentDate,, yyyy/M/d
SendInput %CurrentDate%
Return

::]dl::
FormatTime, CurrentDate,,  yyyy, MMMM d, dddd
SendInput %CurrentDate%
Return

::]dc::
FormatTime, CurrentDate,, yyyy_MM_dd
SendInput %CurrentDate%
Return

::]d1::
FormatTime, CurrentDate,, yyyy-M-d
SendInput %CurrentDate%
Return

::]d2::
FormatTime, CurrentDateTime,, yyyy-MMM-d
SendInput %CurrentDateTime%
Return

::]d3::
FormatTime, CurrentDateTime,, yyyyMMdd
SendInput %CurrentDateTime%
Return

::]d4::
FormatTime, CurrentDateTime,, yyyy-MMM-d
SendInput %CurrentDateTime%
Return

::]d5::
FormatTime, CurrentDateTime,, yyyy.M.d
SendInput %CurrentDateTime%
Return

::]d6::
FormatTime, CurrentDateTime,, yyyy/MM/dd/
SendInput %CurrentDateTime%
Return

::]d7::
FormatTime, CurrentDateTime,, yyyy-MM-dd
SendInput %CurrentDateTime%
Return

::]d8::
FormatTime, CurrentDateTime,, yyyyMMMd
SendInput %CurrentDateTime%
Return

::]d9::
FormatTime, CurrentDateTime,, yyyyMMMdd
SendInput %CurrentDateTime%
Return

::]ymd::
FormatTime, CurrentDateTime,, yyyy-MM-dd
SendInput %CurrentDateTime%
Return

::]t::
FormatTime, Time,, h:mm tt
sendinput %Time%
Return


::]t1::
FormatTime, Time,, H:mm
sendinput %Time%
Return

::]dt::
FormatTime, CurrentDateTime,, yyyy/M/d h:mm tt
SendInput %CurrentDateTime%
Return

::]dt1::
FormatTime, CurrentDateTime,, yyyy-M-d h:mm tt
SendInput %CurrentDateTime%
Return

::]dt2::
FormatTime, CurrentDateTime,,yyyy-MMM-d H:mm
SendInput %CurrentDateTime%
Return

::]dt3::
FormatTime, CurrentDateTime,, yyyy-MMM-dd Thh:mm:ss
SendInput %CurrentDateTime%
Return

::]dt4::
FormatTime, CurrentDateTime,, yyyy-MMM-dd hh:mm:ss
SendInput %CurrentDateTime%
Return

::]dtl::
FormatTime, CurrentDate,, yyyy, MMMM dd, dddd h:mm tt
SendInput %CurrentDate%
Return

^!PrintScreen::		; CTRL + ALT + Print Screen
   FormatTime, xx,, yyyy, MMMM, dd, dddd ; This is one type of the date format
   FormatTime, zz,, h:mm tt ; This is one type of the time format
   SendInput, %xx% %zz%
Return


;******************************************************************************
;			Message Box Greeting - Current Date and Time
;******************************************************************************

::]curdt::
FormatTime, DateTime,, dddd, M/d/yyyy  h:mm tt
Msgbox,
(
Hello FirstName
Today is %DateTime%
)
clipboard = %DateTime%
Return


;******************************************************************************
;			Days of Week
;******************************************************************************
::]mon::Monday
Return

::]tue::Tuesday
Return

::]wed::Wednesday
Return

::]thu::Thursday
Return

::]fri::Friday
Return

::]sat::Saturday
Return

::]sun::Sunday
Return

::]weekdays::Monday, Tuesday, Wednesday, Thursday, Friday
Return

::]weekdays1::Monday{enter}Tuesday{enter}Wednesday{enter}Thursday{enter}Friday
Return

::]weekend::Saturday, Sunday
Return

::]weekend1::Saturday{enter}Sunday
Return

::]week::Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
Return

::]week1::Monday{enter}Tuesday{enter}Wednesday{enter}Thursday{enter}Friday{enter}Saturday{enter}Sunday
Return


;******************************************************************************
;			Months of Year
;******************************************************************************
::]jan::January
Return

::]feb::February
Return

::]mar::March
Return

::]apr::April
Return

::]may::May
Return

::]jun::June
Return

::]jul::July
Return

::]aug::August
Return

::]sep::September
Return

::]oct::October
Return

::]nov::November
Return

::]dec::December
Return


::]1wol::January
Return

::]2wol::February
Return

::]3wol::March
Return

::]4wol::April
Return

::]5wol::May
Return

::]6wol::June
Return

::]7wol::July
Return

::]8wol::August
Return

::]9wol::September
Return

::]10wol::October
Return

::]11wol::November
Return

::]12wol::December
Return



::]months::January, February, March, April, May, June, July, August, September, October, November, December
Return

::]months1::January{enter}February{enter}March{enter}April{enter}May{enter}June{enter}July{enter}August{enter}September{enter}October{enter}November{enter}December
Return


;******************************************************************************
;					Alphabet a-z | A-Z
;******************************************************************************
::]a-z::a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z
Return

::]az::abcdefghijklmnopqrstuvwxyz
Return

::]a-z1::a{enter}b{enter}c{enter}d{enter}e{enter}f{enter}g{enter}h{enter}i{enter}j{enter}k{enter}l{enter}m{enter}n{enter}o{enter}p{enter}q{enter}r{enter}s{enter}t{enter}u{enter}v{enter}w{enter}x{enter}y{enter}z
Return


;******************************************************************************
;			Numbers 1-25 | 1-50 | 1-75 | 1-100
;******************************************************************************
::]1-10::1, 2, 3, 4, 5, 6, 7, 8, 9, 10
Return

::]1-101::1{enter}2{enter}3{enter}4{enter}5{enter}6{enter}7{enter}8{enter}9{enter}10{enter}
Return

::]1-25::1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25
Return

::]1-251::1{enter}2{enter}3{enter}4{enter}5{enter}6{enter}7{enter}8{enter}9{enter}10{enter}11{enter}12{enter}13{enter}14{enter}15{enter}16{enter}17{enter}18{enter}19{enter}20{enter}21{enter}22{enter}23{enter}24{enter}25
Return

::]1-50::1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50
Return

::]1-501::1{enter}2{enter}3{enter}4{enter}5{enter}6{enter}7{enter}8{enter}9{enter}10{enter}11{enter}12{enter}13{enter}14{enter}15{enter}16{enter}17{enter}18{enter}19{enter}20{enter}21{enter}22{enter}23{enter}24{enter}25{enter}26{enter}27{enter}28{enter}29{enter}30{enter}31{enter}32{enter}33{enter}34{enter}35{enter}36{enter}37{enter}38{enter}39{enter}40{enter}41{enter}42{enter}43{enter}44{enter}45{enter}46{enter}47{enter}48{enter}49{enter}50
Return

::]1-75::1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75
Return

::]1-751::1{enter}2{enter}3{enter}4{enter}5{enter}6{enter}7{enter}8{enter}9{enter}10{enter}11{enter}12{enter}13{enter}14{enter}15{enter}16{enter}17{enter}18{enter}19{enter}20{enter}21{enter}22{enter}23{enter}24{enter}25{enter}26{enter}27{enter}28{enter}29{enter}30{enter}31{enter}32{enter}33{enter}34{enter}35{enter}36{enter}37{enter}38{enter}39{enter}40{enter}41{enter}42{enter}43{enter}44{enter}45{enter}46{enter}47{enter}48{enter}49{enter}50{enter}51{enter}52{enter}53{enter}54{enter}55{enter}56{enter}57{enter}58{enter}59{enter}60{enter}61{enter}62{enter}63{enter}64{enter}65{enter}66{enter}67{enter}68{enter}69{enter}70{enter}71{enter}72{enter}73{enter}74{enter}75
Return

::]1-100::1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100
Return

::]1-1001::1{enter}2{enter}3{enter}4{enter}5{enter}6{enter}7{enter}8{enter}9{enter}10{enter}11{enter}12{enter}13{enter}14{enter}15{enter}16{enter}17{enter}18{enter}19{enter}20{enter}21{enter}22{enter}23{enter}24{enter}25{enter}26{enter}27{enter}28{enter}29{enter}30{enter}31{enter}32{enter}33{enter}34{enter}35{enter}36{enter}37{enter}38{enter}39{enter}40{enter}41{enter}42{enter}43{enter}44{enter}45{enter}46{enter}47{enter}48{enter}49{enter}50{enter}51{enter}52{enter}53{enter}54{enter}55{enter}56{enter}57{enter}58{enter}59{enter}60{enter}61{enter}62{enter}63{enter}64{enter}65{enter}66{enter}67{enter}68{enter}69{enter}70{enter}71{enter}72{enter}73{enter}74{enter}75{enter}76{enter}77{enter}78{enter}79{enter}80{enter}81{enter}82{enter}83{enter}84{enter}85{enter}86{enter}87{enter}88{enter}89{enter}90{enter}91{enter}92{enter}93{enter}94{enter}95{enter}96{enter}97{enter}98{enter}99{enter}100
Return


;******************************************************************************
;			Launch applications
;******************************************************************************
::]paint::
Run "c:\Users\minhwasoo\AppData\Local\Microsoft\WindowsApps\mspaint.exe"
Return

::]notepad::
Run "c:\Users\minhwasoo\AppData\Local\Microsoft\WindowsApps\notepad.exe"
Return


;******************************************************************************
;					Open Multiple Websites in Firefox Browser Tabs
;******************************************************************************
::]personal::
Run, msedge.exe https://google.com/ https://www.wikipedia.org/
Return

::]news::
Run, msedge.exe https://www.cnn.com/ https://naver.com/
Return
