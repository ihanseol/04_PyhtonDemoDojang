:: dsk.bat
@ECHO OFF >NUL
@SETLOCAL enableextensions enabledelayedexpansion
set "CheckOnly=0"

set "DoneList="
set "ToDoList="
set "xitem=x"

for %%{ in (%*) do (
  set "_G_found=0"
  echo.
  
  for /F "tokens=1* delims==" %%? in ('doskey /macros') do (
    if /i "%%{"=="%%?" (
      for /F "tokens=*" %%_ in ("%%@") do set "item=%%_"
      if /i "!item:~0,3!"=="for" set "item=!item:%%=%%%%!"
  
      if "%CheckOnly%"=="1" (
          echo :  to do: '!item!'
      ) else (
          echo :  To Do: '!item!'
          call :doItem !item!
      )
      set "DoneList=!DoneList! +%%{"
      set "_G_found=1"
    ) 
  )

  if "!_G_found!"=="0" (
    set "DoneList=!DoneList! -%%{"
    echo :  macro: [%%{] ^(not found^)
    if "!ToDoList!"=="" set "ToDoList=!ToDoList!, [%%{]"
    if "!ToDoList!"=="!ToDoList:[%%{]=!" set "ToDoList=!ToDoList!, [%%{]"
  )
)



echo.
echo :  
echo :    trailing progress report
echo :  
if "%ToDoList%"=="" (
    echo :    all found: %DoneList:~1%
) else (
    echo :    +found, -not found: %DoneList:~1%
    echo :   %ToDoList:~2% not found in macro name list 
)
echo :    end of batch %~f0
echo :  

:endlocal
@ENDLOCAL
@goto :eof

:doItem
  set "xitem=%*"
  set "xitem=%xitem:$T=&%"
  %xitem%

@goto :eof