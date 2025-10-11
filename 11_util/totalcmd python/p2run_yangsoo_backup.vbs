
Set WshShell = CreateObject("WScript.Shell")

' 모든 명령을 '&'로 연결하여 하나의 문자열로 만듭니다.
strCommand = ""
strCommand = strCommand & "cd /d ""c:\Program Files\totalcmd\ini\02_python\03_GroundWater Ussage\23_QT_YangSoo All Step\"" & "
strCommand = strCommand & "call conda activate py311 & "
strCommand = strCommand & "timeout /t 1 >nul & "
strCommand = strCommand & "echo == ""Yangsoo_test_qt.py"" == & "
strCommand = strCommand & "pythonw ""c:\Program Files\totalcmd\ini\02_python\03_GroundWater Ussage\23_QT_YangSoo All Step\yangsoo_test_qt.py"""

' CMD 창을 숨기고 한 번에 실행합니다.
WshShell.Run "cmd /c """ & strCommand & """", 0, True

Set WshShell = Nothing


' VBScript에는 C-스타일의 for 루프(예: for (i=0; i<N; i++))가 없으며, 대신 For...Next 루프를 사용합니다.
' 하지만 요청하신 VBScript는 단순히 여러 개의 명령을 순차적으로 한 번만 실행하는 것이므로, 
' For...Next 루프를 사용할 필요가 없습니다. 루프는 동일한 작업을 반복할 때 사용하는 것입니다.
' 만약 배치 파일의 각 줄을 순회하며 실행하려는 의도였다면 VBScript의 For Each 구문을 사용해야 하지만,
' 현재 코드는 이미 전체 명령 문자열을 한 번에 cmd /c로 실행하고 있으므로 그럴 필요가 없습니다.


' Set WshShell = CreateObject("WScript.Shell")
' ' 명령들을 배열로 정의합니다.
' Dim commands(4)
' commands(0) = "cd /d ""c:\Program Files\totalcmd\ini\02_python\03_GroundWater Ussage\23_QT_YangSoo All Step\"""
' commands(1) = "call conda activate py311"
' commands(2) = "timeout /t 1 >nul"
' commands(3) = "echo == ""Yangsoo_test_qt.py"" =="
' commands(4) = "pythonw ""c:\Program Files\totalcmd\ini\02_python\03_GroundWater Ussage\23_QT_YangSoo All Step\yangsoo_test_qt.py"""

' ' For Each 루프를 사용하여 각 명령을 실행합니다.
' For Each command In commands
'     ' 주의: 각 명령이 독립적인 쉘에서 실행되면 환경 설정(conda, cd)이 유지되지 않습니다.
'     WshShell.Run "cmd /c """ & command & """", 0, True
' Next

' Set WshShell = Nothing



