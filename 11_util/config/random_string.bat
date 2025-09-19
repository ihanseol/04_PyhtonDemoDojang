@echo off
setlocal enabledelayedexpansion

set chars=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
set string=

for /l %%i in (1,1,20) do (
    set /a "rand=!random! %% 62"
    for /f %%j in ('echo !rand!') do set "string=!string!!chars:~%%j,1!"
)

echo !string!



