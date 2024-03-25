@echo off
cd /d d:\05_send

echo Copy d:\05_send folder
:: copy "c:\Program Files\totalcmd\ini\02_python\PDF2ImageConverter.py"   .

echo .
echo Processing ....
python "c:\Program Files\totalcmd\ini\02_python\PDF2ImageConverter.py" 

echo .
echo Processing Complete ...

echo Delaying for 3 seconds...
ping 127.0.0.1 -n 2 > nul


echo and ImageTrim Started ...
python "c:\Program Files\totalcmd\ini\02_python\imageTrim.py"


ping 127.0.0.1 -n 2 > nul


echo delete all aqt files ...
del *.aqt

ping 127.0.0.1 -n 2 > nul
exit /b





