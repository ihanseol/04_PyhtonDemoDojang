Option Explicit

' 필요한 객체 생성
Dim WshShell
Set WshShell = CreateObject("WScript.Shell")

Dim FSO
Set FSO = CreateObject("Scripting.FileSystemObject")

' --- 인수 처리 ---
' 스크립트 인수를 확인
If WScript.Arguments.Count = 0 Then
    WScript.Echo "Usage: cscript exepipe.vbs <CommandToExecute> [OutputFile]"
    WScript.Echo "Example 1 (Default output file): cscript exepipe.vbs p2run_yangsoo.cmd"
    WScript.Echo "Example 2 (Explicit command and output file): cscript exepipe.vbs p2run_yangsoo.cmd p2run_yangsoo.txt"
    WScript.Echo "Example 3 (Simple command): cscript exepipe.vbs dir"
    WScript.Quit 1
End If

Dim strCommand, strOutputFile
Dim strBaseName ' 출력 파일 이름을 위한 명령어의 기본 이름

' 1. 실행할 명령어 설정 (첫 번째 인수)
strCommand = WScript.Arguments(0)
strBaseName = strCommand

' 2. 명령어 기본 이름 설정: 확장자가 없는 경우 처리
Dim intDotPos
intDotPos = InStrRev(strCommand, ".")
If intDotPos > 0 Then
    ' 확장자가 있으면 확장자를 제외한 부분만 기본 이름으로 사용
    strBaseName = Left(strCommand, intDotPos - 1)
End If

' 3. 출력 파일 이름 설정
If WScript.Arguments.Count >= 2 Then
    ' 인수가 2개 이상이면 두 번째 인수를 출력 파일명으로 사용
    strOutputFile = WScript.Arguments(1)
Else
    ' 인수가 1개뿐이면 기본 이름 + ".txt"를 출력 파일명으로 사용
    strOutputFile = strBaseName & ".txt"
End If


' --- 파일 출력 준비 ---

Dim objOutputFile
On Error Resume Next ' 파일 생성 시 오류 무시
' 덮어쓰기 (True) 모드로 파일을 열거나 생성
Set objOutputFile = FSO.CreateTextFile(strOutputFile, True) 
If Err.Number <> 0 Then
    WScript.Echo "Error: Cannot create output file: " & strOutputFile
    WScript.Echo "Error Description: " & Err.Description
    WScript.Quit 1
End If
On Error GoTo 0 ' 오류 처리 다시 활성화

' 실행할 명령어 구성: cmd.exe를 통해 실행하고 2>&1을 사용해 stderr를 stdout으로 리다이렉션
Dim strCmd
' %comspec% 은 cmd.exe 경로를 나타냅니다. /c는 명령 실행 후 종료를 의미합니다.
' 실행할 명령을 따옴표로 감싸서 공백 등이 포함된 파일 이름도 처리 가능하게 합니다.
strCmd = "%comspec% /c """ & strCommand & """ 2>&1"

WScript.Echo "--- Executing: " & strCommand & " ---"
WScript.Echo "--- Output will be saved to: " & strOutputFile & " ---"

' --- 명령어 실행 및 출력 처리 ---

Dim objExec
' Exec 메서드를 사용하여 명령어 실행 및 출력을 캡처
Set objExec = WshShell.Exec(strCmd)

' 실행 중일 때까지 대기하며 출력을 읽고 화면/파일에 기록합니다.
Do While Not objExec.StdOut.AtEndOfStream
    Dim strLine
    ' StdOut에서 한 줄씩 읽기
    strLine = objExec.StdOut.ReadLine()
    
    ' 화면 출력 (cscript에서만 콘솔에 출력됨)
    WScript.Echo strLine
    
    ' 파일에 저장
    objOutputFile.WriteLine strLine
Loop

' 명령어 종료 상태를 확인합니다.
If objExec.ExitCode <> 0 Then
    WScript.Echo "--- Command finished with an error (Exit Code: " & objExec.ExitCode & ") ---"
Else
    WScript.Echo "--- Command finished successfully (Exit Code: " & objExec.ExitCode & ") ---"
End If

' 실행 결과 파일 닫기
objOutputFile.Close

' --- 메모리 정리 ---
Set objExec = Nothing
Set objOutputFile = Nothing
Set WshShell = Nothing
Set FSO = Nothing