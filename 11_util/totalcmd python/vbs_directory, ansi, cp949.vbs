Option Explicit

' ***************************************
' ���� ����
' ***************************************
Dim strNewPath
strNewPath = SelectFolderDialog("������ ���丮�� �����ϼ���.")

If strNewPath <> "" Then
    WScript.Echo "���� ���õ� ���丮: " & strNewPath
    
    ' WScript.Shell ��ü�� ����Ͽ� ���� ���丮�� �����մϴ�.
    ' WScript.Shell ��ü�� Run�̳� Exec �޼��带 ���� �����ϸ�, 
    ' ���� ��ũ��Ʈ�� '�۾� ���丮'�� �����ϴ� �������� VBScript ��ɾ�� �����ϴ�.
    ' ������ BrowseForFolder�� ���õ� ��θ� �޽����� �����ְų�,
    ' ��ũ��Ʈ ������ �ش� ��θ� �������� ���� �۾��� ������ �� �ֽ��ϴ�.
    
    ' ���⼭�� ���õ� ��θ� ������� ���� �Լ��� �����Ͽ� Ȱ�� ���ø� �����ݴϴ�.
    WScript.Echo "--- ���� �Լ� ���� ��� ---"
    
    ' ���� �Լ� 1: ������ ũ�� Ȯ��
    WScript.Echo "1. ���� ũ��: " & GetFolderSize(strNewPath) & " Bytes"
    
    ' ���� �Լ� 2: ���� ���� �� ���� (���� ��ũ��Ʈ ��ġ�� ����)
    Dim strTestFile : strTestFile = "TestLog.txt"
    CreateAndWriteFile strNewPath & "\" & strTestFile, "VBScript �׽�Ʈ �α��Դϴ�."
    WScript.Echo "2. ���� ����: '" & strTestFile & "'��(��) �����Ǿ����ϴ�."
    
    ' ���� �Լ� 3: ���� ���丮�� ���� �� ���
    ' WScript.Echo "3. ���� ���丮�� ���� ��: " & CountFiles(strNewPath) & "��"
    WScript.Echo "3. ���� ���丮�� ���� ��: " & CountFiles(strNewPath)
Else
    WScript.Echo "���丮 ������ ��ҵǾ����ϴ�."
End If

' ***************************************
'  �Լ� 1: ���丮 ���� ���̾�α�
' ***************************************
Function SelectFolderDialog(strMessage)
    ' Shell.Application ��ü�� ����Ͽ� ���� ã�ƺ��� ���̾�α׸� ���ϴ�.
    Const WINDOW_HANDLE = 0  ' â �ڵ� (�׻� 0)
    Const OPTIONS = 0        ' �ɼ� �÷��� (0: �⺻��)
    
    Dim objShell, objFolder, strPath
    Set objShell = CreateObject("Shell.Application")
    
    ' BrowseForFolder(hwnd, Message, Options, RootFolder)
    Set objFolder = objShell.BrowseForFolder(WINDOW_HANDLE, strMessage, OPTIONS)
    
    If Not objFolder Is Nothing Then
        ' ���õ� ������ ��θ� �����ɴϴ�.
        strPath = objFolder.Self.Path
        SelectFolderDialog = strPath
    Else
        ' ��ҵǾ��� ��� �� ���ڿ��� ��ȯ�մϴ�.
        SelectFolderDialog = ""
    End If
    
    Set objShell = Nothing
    Set objFolder = Nothing
End Function

' ***************************************
'  ���� �Լ� 1: ���� ũ�� ��ȯ
' ***************************************
Function GetFolderSize(strFolder)
    Dim objFSO, objFolder
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    
    On Error Resume Next ' ���� �߻� �� �ǳʶ� (��: ���� ���� ����)
    Set objFolder = objFSO.GetFolder(strFolder)
    
    If Err.Number = 0 Then
        GetFolderSize = objFolder.Size
    Else
        GetFolderSize = 0
    End If
    
    On Error GoTo 0 ' ���� ó�� ����
    Set objFSO = Nothing
    Set objFolder = Nothing
End Function

' ***************************************
'  ���� �Լ� 2: ���� ���� �� ���� ����
' ***************************************
Sub CreateAndWriteFile(strFilePath, strContent)
    Dim objFSO, objTS
    Const ForWriting = 2
    
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    
    ' ����� �ɼ� (True)���� �ؽ�Ʈ ������ ���ϴ�. ������ ������ �����մϴ�.
    Set objTS = objFSO.OpenTextFile(strFilePath, ForWriting, True)
    
    objTS.WriteLine strContent
    objTS.Close
    
    Set objFSO = Nothing
    Set objTS = Nothing
End Sub

' ***************************************
'  ���� �Լ� 3: ���� �� ���� ���� ����
' ***************************************
Function CountFiles(strFolder)
    Dim objFSO, objFolder, objFile
    Dim fileCount : fileCount = 0
    
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    
    On Error Resume Next ' ���� �߻� �� �ǳʿ�
    Set objFolder = objFSO.GetFolder(strFolder)
    
    If Err.Number = 0 Then
        For Each objFile In objFolder.Files
            fileCount = fileCount + 1
        Next
    End If
    
    On Error GoTo 0 ' ���� ó�� ����
    CountFiles = fileCount
    
    Set objFSO = Nothing
    Set objFolder = Nothing
End Function