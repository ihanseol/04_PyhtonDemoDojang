@echo off
cd /d d:\05_send

echo Copy d:\05_send folder
:: copy "c:\Program Files\totalcmd\ini\02_python\PDF2ImageConverter.py"   .

echo .
echo Processing ....
python "c:\Program Files\totalcmd\ini\02_python\PDF2ImageConverter.py" 

echo .
echo Processing Complete ...

pause
exit /b








