Set WshShell = CreateObject("WScript.Shell")
' CMD 창을 숨기고 p2run_yangsoo.cmd 배치 파일을 실행합니다.
' 0: 창 숨김, False: 실행이 완료될 때까지 기다리지 않음
WshShell.Run "cmd /c ""p2run_yangsoo.cmd""", 0, True
Set WshShell = Nothing

