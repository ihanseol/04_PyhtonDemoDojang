@echo off

set CMD=%1

echo %CMD%
echo Processing ....
cd /d d:\05_send

if "%CMD%" == "single" (
	python "c:\Program Files\totalcmd\ini\02_python\run_aqt_dontclosefile_refactor.py" single
) else (
	python "c:\Program Files\totalcmd\ini\02_python\run_aqt_dontclosefile_refactor.py" dual
)

echo .
echo Moving PDF file to d:\05_Send
move c:\Users\minhwasoo\Documents\*.pdf d:\05_Send\

echo PDF moving Complete

