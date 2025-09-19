
Sub PasswordBreaker()
    ' Breaks worksheet password protection for all sheets in the workbook.
    
    Dim ws As Worksheet
    Dim i As Integer, j As Integer, k As Integer
    Dim l As Integer, m As Integer, n As Integer
    Dim i1 As Integer, i2 As Integer, i3 As Integer
    Dim i4 As Integer, i5 As Integer, i6 As Integer
    
    On Error Resume Next
    
    For Each ws In ThisWorkbook.Worksheets
        For i = 65 To 66
            For j = 65 To 66
                For k = 65 To 66
                    For l = 65 To 66
                        For m = 65 To 66
                            For i1 = 65 To 66
                                For i2 = 65 To 66
                                    For i3 = 65 To 66
                                        For i4 = 65 To 66
                                            For i5 = 65 To 66
                                                For i6 = 65 To 66
                                                    For n = 32 To 126
                                                        ws.Unprotect Chr(i) & Chr(j) & Chr(k) & _
                                                                      Chr(l) & Chr(m) & Chr(i1) & _
                                                                      Chr(i2) & Chr(i3) & Chr(i4) & _
                                                                      Chr(i5) & Chr(i6) & Chr(n)
                                                        If ws.ProtectContents = False Then
                                                            MsgBox "Password for sheet " & ws.Name & " is " & _
                                                                   Chr(i) & Chr(j) & Chr(k) & Chr(l) & Chr(m) & _
                                                                   Chr(i1) & Chr(i2) & Chr(i3) & Chr(i4) & Chr(i5) & _
                                                                   Chr(i6) & Chr(n)
                                                            Exit For
                                                        End If
                                                    Next n
                                                    If ws.ProtectContents = False Then Exit For
                                                Next i6
                                                If ws.ProtectContents = False Then Exit For
                                            Next i5
                                            If ws.ProtectContents = False Then Exit For
                                        Next i4
                                        If ws.ProtectContents = False Then Exit For
                                    Next i3
                                    If ws.ProtectContents = False Then Exit For
                                Next i2
                                If ws.ProtectContents = False Then Exit For
                            Next i1
                            If ws.ProtectContents = False Then Exit For
                        Next m
                        If ws.ProtectContents = False Then Exit For
                    Next l
                    If ws.ProtectContents = False Then Exit For
                Next k
                If ws.ProtectContents = False Then Exit For
            Next j
            If ws.ProtectContents = False Then Exit For
        Next i
    Next ws
End Sub

