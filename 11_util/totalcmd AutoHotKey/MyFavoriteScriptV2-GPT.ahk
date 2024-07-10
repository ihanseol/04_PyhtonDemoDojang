;*******************************************************************************
; Title:          My fav AHK scripts
; Description:    AutoHotkey scripts that make my daily life a bit easier :)
; Author:         How To Work From Home
;*******************************************************************************

; Keyboard shortcuts Matrix
; (hash)                #    Windows logo key
; (exclamation mark)    !    ALT
; (caret)               ^    CTRL
; (plus)                +    Shift


;******************************************************************************
;			Reload/Execute this script.ahk file
;******************************************************************************
;::rscript::


#Requires AutoHotkey v2.0
#SingleInstance


^!R:: ; CTRL + ALT + R
{
    ; Run the script again to simulate reload
    SendInput("misssn")
    Run("c:\Program Files\totalcmd\ini\03_AutoHotKey\MyFavoriteScript.ahk")
}

^e::ExitApp

;******************************************************************************
;			Text replacements for most used keywords
;******************************************************************************

::]pr::Print('hello world')
::]ty::Thank you,
::]tyxx::Thank you,`nFirstName LastName
::]yw::You're Welcome
::]myph::123-456-7890
::]mycell::098-765-4321
::]ol::first.last@outlook.com
::]hm::first.last@hotmail.com
::]gm::first.last@gmail.com
::]ym::first.last@yahoo.com




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
::]myid::Send(A_UserName)
::]myip::Send(A_IPAddress1)
::]mycomp::Send(A_ComputerName)



;******************************************************************************
;			Dash lines
;******************************************************************************
::]-10::----------
::]-20::--------------------
::]-30::------------------------------
::]-40::----------------------------------------
::]-50::--------------------------------------------------
::]*10::**********
::]*20::********************
::]*30::******************************
::]*40::****************************************
::]*50::**************************************************



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
::]sel*::
(
SELECT *
FROM
WHERE 1 = 1
AND ROWNUM <= 10
-- AND Field_value_1 = upper('value')
-- AND upper(Field_value_2) LIKE upper('%value%')
)

;******************************************************************************
;			Date/Time Stamps
;******************************************************************************


::F1::
{
    ; Get the current date and time in the specified format
    CurrentDateTime := FormatTime("yyyy MMMM d, HH:mm:ss", A_Now)

    ; Match the date and time components using RegEx
    if (RegExMatch(CurrentDateTime, "(\d+) (\w+) (\d+), (\d+):(\d+):(\d+)", &Match))
    {
        ; Convert the captured month name to a month index
        MonthNames := ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        Loop 12
        {
            if (MonthNames[A_Index] = Match[2])
            {
                Month := MonthNames[A_Index]
                break
            }
        }

        ; Send the formatted date and month
        SendInput(CurrentDateTime ", " Month)
    }
}




::]d::SendInput(FormatTime(, A_Now))
::]dl::SendInput(Format("{:yyyy, MMMM d, dddd}", A_Now))
::]dc::SendInput(Format("{:yyyy_MM_dd}", A_Now))
::]d1::SendInput(Format("{:yyyy-M-d}", A_Now))
::]d2::SendInput(Format("{:yyyy-MMM-d}", A_Now))
::]d3::SendInput(Format("{:yyyyMMdd}", A_Now))
::]d4::SendInput(Format("{:yyyy-MMM-d}", A_Now))
::]d5::SendInput(Format("{:yyyy.M.d}", A_Now))
::]d6::SendInput(Format("{:yyyy/MM/dd/}", A_Now))
::]d7::SendInput(Format("{:yyyy-MM-dd}", A_Now))
::]d8::SendInput(Format("{:yyyyMMMd}", A_Now))
::]d9::SendInput(Format("{:yyyyMMMdd}", A_Now))
::]ymd::SendInput(Format("{:yyyy-MM-dd}", A_Now))
::]t::SendInput(Format("{:h:mm tt}", A_Now))
::]t1::SendInput(Format("{:H:mm}", A_Now))
::]dt::SendInput(Format("{:yyyy/M/d h:mm tt}", A_Now))
::]dt1::SendInput(Format("{:yyyy-M-d h:mm tt}", A_Now))
::]dt2::SendInput(Format("{:yyyy-MMM-d H:mm}", A_Now))
::]dt3::SendInput(Format("{:yyyy-MMM-dd Thh:mm:ss}", A_Now))
::]dt4::SendInput(Format("{:yyyy-MMM-dd hh:mm:ss}", A_Now))

;~ ::]dtl::SendInput(Format("{:yyyy, MMMM dd, dddd h:mm tt}", A_Now))



^!PrintScreen::
{
    xx := FormatTime("yyyy, MMMM, dd, dddd", A_Now)
    zz := FormatTime("h:mm tt", A_Now)
    SendInput(xx " " zz)
}

;******************************************************************************
;			Message Box Greeting - Current Date and Time
;*****************************************************************************



::]curdt::
{
    ;~ FormatTime, DateTime,, "dddd, M/d/yyyy  h:mm tt"

	DateTime := FormatTime("yyyy MMMM d, HH:mm:ss", A_Now)

    MsgBox "Hello FirstName`nToday is " DateTime
    Clipboard := DateTime
}



;******************************************************************************
;			Days of Week
;******************************************************************************
::]mon::Monday
::]tue::Tuesday
::]wed::Wednesday
::]thu::Thursday
::]fri::Friday
::]sat::Saturday
::]sun::Sunday
::]weekdays::Monday, Tuesday, Wednesday, Thursday, Friday
::]weekdays1::Monday`nTuesday`nWednesday`nThursday`nFriday
::]weekend::Saturday, Sunday
::]weekend1::Saturday`nSunday
::]week::Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
::]week1::Monday`nTuesday`nWednesday`nThursday`nFriday`nSaturday`nSunday

;******************************************************************************
;			Months of Year
;******************************************************************************
::]jan::January
::]feb::February
::]mar::March
::]apr::April
::]may::May
::]jun::June
::]jul::July
::]aug::August
::]sep::September
::]oct::October
::]nov::November
::]dec::December
::]1wol::January
::]2wol::February
::]3wol::March
::]4wol::April
::]5wol::May
::]6wol::June
::]7wol::July
::]8wol::August
::]9wol::September
::]10wol::October
::]11wol::November
::]12wol::December
::]months::January, February, March, April, May, June, July, August, September, October, November, December
::]months1::January`nFebruary`nMarch`nApril`nMay`nJune`nJuly`nAugust`nSeptember`nOctober`nNovember`nDecember



;******************************************************************************
;					Alphabet a-z | A-Z
;******************************************************************************
::]a-z::a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z
::]az::abcdefghijklmnopqrstuvwxyz
::]a-z1::a`nb`nc`nd`ne`nf`ng`nh`ni`nj`nk`nl`nm`nn`no`np`nq`nr`ns`nt`nu`nv`nw`nx`ny`nz
::]a::a
::]b::b
::]c::c
::]d::d
::]e::e
::]f::f
::]g::g
::]h::h
::]i::i
::]j::j
::]k::k
::]l::l
::]m::m
::]n::n
::]o::o
::]p::p
::]q::q
::]r::r
::]s::s
::]t::t
::]u::u
::]v::v
::]w::w
::]x::x
::]y::y
::]z::z

::]A-Z::A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z
::]AZ::ABCDEFGHIJKLMNOPQRSTUVWXYZ
::]A-Z1::A`nB`nC`nD`nE`nF`nG`nH`nI`nJ`nK`nL`nM`nN`nO`nP`nQ`nR`nS`nT`nU`nV`nW`nX`nY`nZ

;******************************************************************************
;			1-10 Numbers | Ordinal numbers
;******************************************************************************
::]0-9::1, 2, 3, 4, 5, 6, 7, 8, 9
::]1st-10th::1st, 2nd, 3rd, 4th, 5th, 6th, 7th, 8th, 9th, 10th

;******************************************************************************
;			Windows Information
;******************************************************************************
;~ ^+i::
;~ {
    ;~ WinGetTitle, currentWindowTitle, A
    ;~ WinGetClass, currentWindowClass, A
    ;~ WinGet, currentWindowID, ID, A
    ;~ WinGet, currentWindowProcess, ProcessName, A

    ;~ clipboard := "Title: " currentWindowTitle "`nClass: " currentWindowClass "`nID: " currentWindowID "`nProcess: " currentWindowProcess
    ;~ MsgBox clipboard
;~ }


^+i::
{
    ; Get the title of the current active window
    currentWindowTitle := WinGetTitle("A")

    ; Get the class of the current active window
    currentWindowClass := WinGetClass("A")

    ; Get the ID of the current active window
    currentWindowID := WinGetID("A")

    ; Get the process name of the current active window
    currentWindowProcess := WinGetProcessName("A")

    ; Set the clipboard content
    clipboard := "Title: " currentWindowTitle "`nClass: " currentWindowClass "`nID: " currentWindowID "`nProcess: " currentWindowProcess

    ; Show the clipboard content in a message box
    MsgBox(clipboard)
}




; End of script
