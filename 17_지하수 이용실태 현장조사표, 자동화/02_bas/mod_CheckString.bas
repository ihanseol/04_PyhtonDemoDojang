Attribute VB_Name = "mod_CheckString"
Option Explicit


Function CheckSubstring(str As String, chk As String) As Boolean
    
    If InStr(str, chk) > 0 Then
        ' The string contains "chk"
        CheckSubstring = True
    Else
        ' The string does not contain "chk"
        CheckSubstring = False
    End If
End Function


Function IsDrinking(str As String) As Boolean
    
    ' ������ - �缳
    If CheckSubstring(str, "����") Then
            IsDrinking = True
            Exit Function
    End If
    
    ' �Ϲݿ� - �缳
    If CheckSubstring(str, "�Ϲ�") Then
           IsDrinking = False
            Exit Function
    End If
    
    ' �б��� - ����
    If CheckSubstring(str, "�б�") Then
             IsDrinking = True
            Exit Function
    End If
        
    ' �ι����� - ����
    If CheckSubstring(str, "�ι�") Then
             IsDrinking = False
            Exit Function
    End If
    
    ' �������ÿ� - �缳
    If CheckSubstring(str, "����") Then
             IsDrinking = True
            Exit Function
    End If
    
    ' ���̻���� - ����
    If CheckSubstring(str, "����") Then
             IsDrinking = True
            Exit Function
    End If
    
    ' ���Ȱ��� - �缳
    If CheckSubstring(str, "���") Then
             IsDrinking = False
            Exit Function
    End If
    
    ' ��Ÿ - �缳
    If CheckSubstring(str, "��Ÿ") Then
             IsDrinking = False
            Exit Function
    End If
    
    IsDrinking = False
       
End Function



Function SS_StringCheck(str As String) As String
    
    ' ������ - �缳
    If CheckSubstring(str, "����") Then
            SS_StringCheck = "g,"
            Exit Function
    End If
    
    ' �Ϲݿ� - �缳
    If CheckSubstring(str, "�Ϲ�") Then
            SS_StringCheck = "h,"
            Exit Function
    End If
    
    ' �б��� - ����
    If CheckSubstring(str, "�б�") Then
            SS_StringCheck = "i,"
            Exit Function
    End If
        
    ' �ι����� - ����
    If CheckSubstring(str, "�ι�") Then
            SS_StringCheck = "j,"
            Exit Function
    End If
    
    ' �������ÿ� - �缳
    If CheckSubstring(str, "����") Then
            SS_StringCheck = "k,"
            Exit Function
    End If
    
    ' ���̻���� - ����
    If CheckSubstring(str, "����") Then
            SS_StringCheck = "l,"
            Exit Function
    End If
    
    ' ���Ȱ��� - �缳
    If CheckSubstring(str, "���") Then
            SS_StringCheck = "m,"
            Exit Function
    End If
    
    ' ��Ÿ - �缳
    If CheckSubstring(str, "��Ÿ") Then
            SS_StringCheck = "n,"
            Exit Function
    End If
    
    SS_StringCheck = "n,"
    
    

End Function

Function AA_StringCheck(str As String) As String
    
    ' ������� ���� �缳, ���� �㰡�� - ����
    If CheckSubstring(str, "����") Then
            AA_StringCheck = "v,"
            Exit Function
    End If
    
    If CheckSubstring(str, "����") Then
            AA_StringCheck = "w,"
            Exit Function
    End If
    
    If CheckSubstring(str, "����") Then
            AA_StringCheck = "x,"
            Exit Function
    End If
    
    If CheckSubstring(str, "���") Then
            AA_StringCheck = "y,"
            Exit Function
    End If
    
    If CheckSubstring(str, "���") Then
            AA_StringCheck = "z,"
            Exit Function
    End If
    
    If CheckSubstring(str, "��Ÿ") Then
            AA_StringCheck = "aa,"
            Exit Function
    End If
    
    AA_StringCheck = "aa,"
    
End Function


Function II_StringCheck(str As String) As String
    
    ' �ذ�, ����, ��� - ����
    If CheckSubstring(str, "����") Then
            II_StringCheck = "p,"
            Exit Function
    End If
    
    If CheckSubstring(str, "����") Then
            II_StringCheck = "q,"
            Exit Function
    End If
    
    If CheckSubstring(str, "���") Then
            II_StringCheck = "r,"
            Exit Function
    End If
    
    ' ��������, ��Ÿ - �缳
    If CheckSubstring(str, "��������") Then
            II_StringCheck = "s,"
            Exit Function
    End If
    
    If CheckSubstring(str, "��Ÿ") Then
            II_StringCheck = "t,"
            Exit Function
    End If

    II_StringCheck = "t,"
End Function



Function SS_PublicCheck(str As String) As String
    
    ' ������ - �缳
    If CheckSubstring(str, "����") Then
            SS_PublicCheck = "ac,"
            Exit Function
    End If
    
    ' �Ϲݿ� - �缳
    If CheckSubstring(str, "�Ϲ�") Then
            SS_PublicCheck = "ac,"
            Exit Function
    End If
    
    ' �б��� - ����
    If CheckSubstring(str, "�б�") Then
            SS_PublicCheck = "ab,"
            Exit Function
    End If
        
    ' �ι����� - ����
    If CheckSubstring(str, "�ι�") Then
            SS_PublicCheck = "ab,"
            Exit Function
    End If
    
    ' �������ÿ� - �缳
    If CheckSubstring(str, "����") Then
            SS_PublicCheck = "ac,"
            Exit Function
    End If
    
    ' ���̻���� - ����
    If CheckSubstring(str, "����") Then
            SS_PublicCheck = "ab,"
            Exit Function
    End If
    
    ' ���Ȱ��� - �缳
    If CheckSubstring(str, "���") Then
            SS_PublicCheck = "ac,"
            Exit Function
    End If
    
    ' ��Ÿ - �缳
    If CheckSubstring(str, "��Ÿ") Then
            SS_PublicCheck = "ac,"
            Exit Function
    End If
    
    SS_PublicCheck = "ac,"

End Function

Function AA_PublicCheck(str As String) As String
    
    ' ������� ���� �缳, ���� �㰡�� - ����
    If CheckSubstring(str, "����") Then
            AA_PublicCheck = "ac,"
            Exit Function
    End If
    
    If CheckSubstring(str, "����") Then
            AA_PublicCheck = "ac,"
            Exit Function
    End If
    
    If CheckSubstring(str, "����") Then
            AA_PublicCheck = "ac,"
            Exit Function
    End If
    
    If CheckSubstring(str, "���") Then
            AA_PublicCheck = "ac,"
            Exit Function
    End If
    
    If CheckSubstring(str, "���") Then
            AA_PublicCheck = "ac,"
            Exit Function
    End If
    
    If CheckSubstring(str, "��Ÿ") Then
            AA_PublicCheck = "ac,"
            Exit Function
    End If
    
    AA_PublicCheck = "ac,"
    
End Function


Function II_PublicCheck(str As String) As String
    
    ' �ذ�, ����, ��� - ����
    If CheckSubstring(str, "����") Then
            II_PublicCheck = "ab,"
            Exit Function
    End If
    
    If CheckSubstring(str, "����") Then
            II_PublicCheck = "ab,"
            Exit Function
    End If
    
    If CheckSubstring(str, "���") Then
            II_PublicCheck = "ab,"
            Exit Function
    End If
    
    ' ��������, ��Ÿ - �缳
    If CheckSubstring(str, "��������") Then
            II_PublicCheck = "ac,"
            Exit Function
    End If
    
    If CheckSubstring(str, "��Ÿ") Then
            II_PublicCheck = "ac,"
            Exit Function
    End If

    II_PublicCheck = "ac,"
    
End Function


