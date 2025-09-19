"""
Sub get_weather_data()
    Dim driver As New chromeDriver
    Dim ddl As Selenium.SelectElement

    Dim loginIdElement As Selenium.WebElement
    Dim passwordElement As Selenium.WebElement


    Dim url As String
    Dim one_string, two_string As String
    Dim sYear, eYear As Integer
    Dim str As String

    Range("B2").Value = "30년 " & Range("S8").Value & "데이터, " & Now()

    url = "https://data.kma.go.kr/stcs/grnd/grndRnList.do?pgmNo=69"
    Set driver = New Selenium.chromeDriver

    ' driver.SetBinary "c:\ProgramData\00_chrome\chrome.exe" ' Update this path

    driver.Start
    driver.AddArgument "--headless"
    driver.Window.Maximize
    driver.Get url

    Sleep (1 * 1000)


    ' 2025-6-11, id, pw
    ' #loginBtn


    driver.FindElementByCss("#loginBtn").Click
    Sleep (1 * 1000)

    '#loginId
    '#passwordNo
    Set loginIdElement = driver.FindElementByCss("#loginId")
    loginIdElement.SendKeys "hanseol33@naver.com"
    Sleep (1 * 1000)

    Set passwordElement = driver.FindElementByCss("#passwordNo")
    passwordElement.SendKeys "dseq%z8^feyham^"
    Sleep (1 * 1000)

    driver.FindElementByCss("#loginbtn").Click
    Sleep (1 * 1000)


    '2023/10/28 일, 홈페이지 코드가 변경됨 ...
    ' id="ztree_61_switch"
    ' <a href="javascript:;" id="ztree_61_switch" onclick="treeBtChange(this)" class="button level1 switch center_close" treenode_switch=""><span class="blind">열기</span></a>
    ' #ztree_61_switch, selector복사로 취득

    one_string = "ztree_" & CStr(Range("S10").Value) & "_switch"


    If Range("R9").Value = "Table7" Then
    two_string = Range("S8").Value
    Else
    two_string = Range("S8").Value & " (" & CStr(Range("S9").Value) & ")"
    End If

    '금산 (238)

    Set ddl = driver.FindElementByCss("#dataFormCd").AsSelect
    ddl.SelectByText ("월")
    Sleep (0.5 * 1000)


    ' ---------------------------------------------------------------

    driver.FindElementByCss("#txtStnNm").Click
    Sleep (1 * 1000)

    driver.FindElementByCss("#" & one_string).Click
    Sleep (1 * 1000)

    driver.FindElementByLinkText(two_string).Click
    Sleep (1 * 1000)

    driver.FindElementByLinkText("선택완료").Click


    ' ---------------------------------------------------------------
    ' 시작년도, 끝년도 삽입

    eYear = Year(Now()) - 1
    sYear = eYear - 29

    Set ddl = driver.FindElementByCss("#startYear").AsSelect
    ddl.SelectByText (CStr(sYear))
    Sleep (0.5 * 1000)

    Set ddl = driver.FindElementByCss("#endYear").AsSelect
    ddl.SelectByText (CStr(eYear))
    Sleep (0.5 * 1000)
    ' ---------------------------------------------------------------

    ' Search Button
    ' driver.FindElementByXPath("//*[@id=
    'schFor
    m']/div[2]").Click
    ' copy by selector

    '검색 버튼클릭
    ' driver.FindElementByCss("#schForm > div.wrap_btn > button").Click
    driver.FindElementByCss("button.SEARCH_BTN").Click


    Sleep (2 * 1000)

    ' Excel download button
    ' driver.FindElementByLinkText("Excel").Click


    'Excel download
    ' driver.FindElementByCss("#wrap_content > div:nth-child(15) > div.hd_itm > div > a.DOWNLOAD_BTN_XLS").Click

    'CSV download
    ' driver.FindElementByCss("#wrap_content > div:nth-child(15) > div.hd_itm > div > a.DOWNLOAD_BTN").Click
    driver.FindElementByCss("a.DOWNLOAD_BTN").Click


    Sleep (3 * 1000)s

End Sub

"""