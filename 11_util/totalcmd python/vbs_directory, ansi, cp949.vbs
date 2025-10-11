Option Explicit

' ***************************************
' 메인 로직
' ***************************************
Dim strNewPath
strNewPath = SelectFolderDialog("변경할 디렉토리를 선택하세요.")

If strNewPath <> "" Then
    WScript.Echo "새로 선택된 디렉토리: " & strNewPath
    
    ' WScript.Shell 객체를 사용하여 현재 디렉토리를 변경합니다.
    ' WScript.Shell 객체는 Run이나 Exec 메서드를 위해 존재하며, 
    ' 현재 스크립트의 '작업 디렉토리'를 변경하는 직접적인 VBScript 명령어는 없습니다.
    ' 하지만 BrowseForFolder로 선택된 경로를 메시지로 보여주거나,
    ' 스크립트 내에서 해당 경로를 기준으로 파일 작업을 수행할 수 있습니다.
    
    ' 여기서는 선택된 경로를 기반으로 샘플 함수를 실행하여 활용 예시를 보여줍니다.
    WScript.Echo "--- 샘플 함수 실행 결과 ---"
    
    ' 샘플 함수 1: 폴더의 크기 확인
    WScript.Echo "1. 폴더 크기: " & GetFolderSize(strNewPath) & " Bytes"
    
    ' 샘플 함수 2: 파일 생성 및 쓰기 (현재 스크립트 위치에 생성)
    Dim strTestFile : strTestFile = "TestLog.txt"
    CreateAndWriteFile strNewPath & "\" & strTestFile, "VBScript 테스트 로그입니다."
    WScript.Echo "2. 파일 생성: '" & strTestFile & "'이(가) 생성되었습니다."
    
    ' 샘플 함수 3: 현재 디렉토리의 파일 수 계산
    ' WScript.Echo "3. 현재 디렉토리의 파일 수: " & CountFiles(strNewPath) & "개"
    WScript.Echo "3. 현재 디렉토리의 파일 수: " & CountFiles(strNewPath)
Else
    WScript.Echo "디렉토리 선택이 취소되었습니다."
End If

' ***************************************
'  함수 1: 디렉토리 선택 다이얼로그
' ***************************************
Function SelectFolderDialog(strMessage)
    ' Shell.Application 객체를 사용하여 폴더 찾아보기 다이얼로그를 엽니다.
    Const WINDOW_HANDLE = 0  ' 창 핸들 (항상 0)
    Const OPTIONS = 0        ' 옵션 플래그 (0: 기본값)
    
    Dim objShell, objFolder, strPath
    Set objShell = CreateObject("Shell.Application")
    
    ' BrowseForFolder(hwnd, Message, Options, RootFolder)
    Set objFolder = objShell.BrowseForFolder(WINDOW_HANDLE, strMessage, OPTIONS)
    
    If Not objFolder Is Nothing Then
        ' 선택된 폴더의 경로를 가져옵니다.
        strPath = objFolder.Self.Path
        SelectFolderDialog = strPath
    Else
        ' 취소되었을 경우 빈 문자열을 반환합니다.
        SelectFolderDialog = ""
    End If
    
    Set objShell = Nothing
    Set objFolder = Nothing
End Function

' ***************************************
'  샘플 함수 1: 폴더 크기 반환
' ***************************************
Function GetFolderSize(strFolder)
    Dim objFSO, objFolder
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    
    On Error Resume Next ' 에러 발생 시 건너뜀 (예: 접근 권한 없음)
    Set objFolder = objFSO.GetFolder(strFolder)
    
    If Err.Number = 0 Then
        GetFolderSize = objFolder.Size
    Else
        GetFolderSize = 0
    End If
    
    On Error GoTo 0 ' 에러 처리 복구
    Set objFSO = Nothing
    Set objFolder = Nothing
End Function

' ***************************************
'  샘플 함수 2: 파일 생성 및 내용 쓰기
' ***************************************
Sub CreateAndWriteFile(strFilePath, strContent)
    Dim objFSO, objTS
    Const ForWriting = 2
    
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    
    ' 덮어쓰기 옵션 (True)으로 텍스트 파일을 엽니다. 파일이 없으면 생성합니다.
    Set objTS = objFSO.OpenTextFile(strFilePath, ForWriting, True)
    
    objTS.WriteLine strContent
    objTS.Close
    
    Set objFSO = Nothing
    Set objTS = Nothing
End Sub

' ***************************************
'  샘플 함수 3: 폴더 내 파일 개수 세기
' ***************************************
Function CountFiles(strFolder)
    Dim objFSO, objFolder, objFile
    Dim fileCount : fileCount = 0
    
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    
    On Error Resume Next ' 에러 발생 시 건너옴
    Set objFolder = objFSO.GetFolder(strFolder)
    
    If Err.Number = 0 Then
        For Each objFile In objFolder.Files
            fileCount = fileCount + 1
        Next
    End If
    
    On Error GoTo 0 ' 에러 처리 복구
    CountFiles = fileCount
    
    Set objFSO = Nothing
    Set objFolder = Nothing
End Function