var WshShell = new ActiveXObject("WScript.Shell");

// 모든 명령을 '&'로 연결하여 하나의 문자열로 만듭니다.
var strCommand = "";
strCommand = strCommand + "cd /d \"c:\\Program Files\\totalcmd\\ini\\02_python\\03_GroundWater Ussage\\23_QT_YangSoo All Step\\\" & ";
strCommand = strCommand + "call conda activate py311 & ";
strCommand = strCommand + "timeout /t 1 >nul & ";
strCommand = strCommand + "echo == \"Yangsoo_test_qt.py\" == & ";
strCommand = strCommand + "python \"c:\\Program Files\\totalcmd\\ini\\02_python\\03_GroundWater Ussage\\23_QT_YangSoo All Step\\yangsoo_test_qt.py\"";

// CMD 창을 숨기고 한 번에 실행합니다.
// Run 메서드의 인수는 (Command, WindowStyle, WaitOnReturn) 입니다.
// WindowStyle 0은 창을 숨깁니다.
// WaitOnReturn true는 명령이 완료될 때까지 스크립트 실행을 기다립니다.
WshShell.Run("cmd /c \"" + strCommand + "\"", 0, true);

WshShell = null;

