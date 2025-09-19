@echo off

if  "%PROCESSOR_ARCHITECTURE%"=="x86" (
    set "commander_name=TOTALCMD.EXE"
    echo System is x86
) else (
    set "commander_name=TOTALCMD64.EXE"
    echo System is x64
)

tasklist | find /i "%commander_name%" && taskkill /im "%commander_name%" /F || echo process "%commander_name%" not running.


echo argument : "%~1"
set "arg=%~1"


if not "%arg%" == "" (
  echo Argument defined: %arg%
) else (  
  echo Usage: script.bat "<rar_file_name>"
  exit /b 1
)

::set "source_rar=%~1"
set "source_rar=%~1"
set "desktop_path=%userprofile%\Desktop"

echo Desktop path: %desktop_path%
set "target_dir=%desktop_path%"

echo --------------------------------------------------------------------
echo source file : %source_rar%
echo target directory : %target_dir%
echo --------------------------------------------------------------------
echo Extract %source_rar% ....

"C:\Program Files\WinRAR\winrar.exe" x -y "%source_rar%" -op "%target_dir%"

echo delete tatalcmd directory ...

echo --------------------------------------------------------------------

if exist "c:\Program Files\totalcmd" (
    rmdir /s /q "c:\Program Files\totalcmd"
)


echo Done waiting.

set "src_folder=%userprofile%\Desktop\totalcmd"
set "dst_folder=c:\Program Files\totalcmd"


echo --------------------------------------------------------------------
echo Source Folder : %src_folder%
echo Destination Folder : %dst_folder%
echo --------------------------------------------------------------------

move  "%src_folder%" "%dst_folder%"





