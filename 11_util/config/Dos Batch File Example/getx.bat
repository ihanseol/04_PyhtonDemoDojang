::getx %envvar% [\m]
::reads envvar from user enviroment variable and stores it in getxvalue variable
::with \m read system enviroment

@SETLOCAL EnableDelayedExpansion
@echo OFF

@set l_regpath="HKEY_CURRENT_USER\Environment"
@if "\m"=="%2" set l_regpath="HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"

::REG ADD "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH /t REG_SZ /f /d "%PATH%"
::@REG QUERY %l_regpath% /v %1 /S

@FOR /F "tokens=*" %%A IN ('REG QUERY %l_regpath% /v %1 /S') DO (
@  set l_a=%%A
@   if NOT "!l_a!"=="!l_a:    =!" set l_line=!l_a! 
)

::delimiter is four spaces change it to tab \t
@set l_line=!l_line!
@set l_line=%l_line:    =   %

@set getxvalue=

@FOR /F "tokens=3* delims=  " %%A IN ("%l_line%") DO (
@   set getxvalue=%%A
)
@set getxvalue=!getxvalue!
@echo %getxvalue% > getxfile.tmp.txt
@ENDLOCAL

::we already used tab as delimiter
@FOR /F "delims=    " %%A IN (getxfile.tmp.txt) DO (
    @set getxvalue=%%A
)
@del getxfile.tmp.txt

@echo ON