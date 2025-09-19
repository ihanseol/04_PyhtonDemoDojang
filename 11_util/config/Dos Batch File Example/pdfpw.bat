@ECHO OFF

setlocal EnableDelayedExpansion
md out
for /f %%G in ('dir /b "*.pdf"') do (
	call:_pwgen passwd
	pdftk %%G output out/%%G user_pw !passwd!
	echo '%%G', '!passwd!' >> out/passwords.csv
)

goto :EOF

:_pwgen passwd
setlocal ENABLEEXTENSIONS
set _RNDLength=8
set _Alphanumeric=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
set _Str=%_Alphanumeric%987654321
set passwd=%~1
:_LenLoop
if not "%_Str:~18%"=="" set _Str=%_Str:~9%& set /A _Len+=9& GOTO :_LenLoop
set _tmp=%_Str:~9,1%
set /A _Len=_Len+_tmp
set _count=0
set _RndAlphaNum=
:_loop
set /a _count+=1
set _RND=%Random%
set /A _RND=_RND%%%_Len%
set _RndAlphaNum=!_RndAlphaNum!!_Alphanumeric:~%_RND%,1!
if !_count! lss %_RNDLength% goto _loop
set passwd=!_RndAlphaNum!
endlocal&set %~1=%passwd%
GOTO:EOF