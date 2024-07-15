 
; Language: English
; Platform: Win9x/Nt
; Author: How to work from home


;**************************************************************
; Current Window Title to Clipboard - CTRL + ALT + i
;**************************************************************

^!i::
WinGetActiveTitle, Title
String = %Title%
Clipboard = %Title%
return













