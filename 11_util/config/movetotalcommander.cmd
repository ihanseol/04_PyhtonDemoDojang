
@echo off

:: C:\Program Files

cd /d "c:\Users\minhwasoo\Desktop\"
rmdir /s /q "C:\Program Files\totalcmd" 

:: xcopy totalcmd "C:\Program Files\totalcmd" /e /h /c /i
move totalcmd "C:\Program Files\totalcmd" 

pause


