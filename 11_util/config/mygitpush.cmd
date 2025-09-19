:: @echo off

@echo off
SET CMD=%~1

:: Get the current timestamp and save it to a file
for /f "tokens=*" %%t in ('powershell -command "Get-Date -Format 'yyyyMMddHHmmss'"') do set timestamp=%%t
echo %timestamp% > timestamp.txt

:: Generate MD5 hash and extract only the hash value
for /f "skip=1 tokens=1" %%h in ('certutil -hashfile timestamp.txt MD5 ^| findstr /v "hash CertUtil"') do set hash=%%h

:: Display the hash
echo MD5 Hash: %hash%
del timestamp.txt


IF "%CMD%" == "" (
  GOTO allpush
)

if "%CMD%" == "1" goto 01_Linux
::if "%CMD%" == "2" goto 02_Excel
::if "%CMD%" == "22" goto 02_Excel2
if "%CMD%" == "23" goto 02_Excel3
if "%CMD%" == "3" goto 03_visual_lisp
if "%CMD%" == "4" goto 04_PyhtonDemoDojang
if "%CMD%" == "5" goto 05_JAVA
if "%CMD%" == "6" goto 06_DELPHI
if "%CMD%" == "7" goto 07_AutoIT


@echo on



:01_Linux
@echo.
@echo -------------------------------------------------
@echo   01_Linux 
@echo -------------------------------------------------
@echo.


cd /d d:/12_dev/01_Linux

git status
git add .
git commit -m %hash%
git push 
goto exit


:02_Excel

@echo.
@echo -------------------------------------------------
@echo   02_Excel
@echo -------------------------------------------------
@echo.

cd /d d:/12_dev/02_Excel

git status
git add .
git commit -m %hash%
git push 
goto exit

:02_Excel2

@echo.
@echo -------------------------------------------------
@echo   02_Excel2
@echo -------------------------------------------------
@echo.

cd /d d:/12_dev/02_Excel2

git status
git add .
git commit -m %hash%
git push
goto exit


:02_Excel3

@echo.
@echo -------------------------------------------------
@echo   02_Excel3
@echo -------------------------------------------------
@echo.

cd /d d:/12_dev/02_Excel3

git status
git add .
git commit -m %hash%
git push origin main
goto exit


:03_visual_lisp

@echo.
@echo -------------------------------------------------
@echo   03_visual_lisp
@echo -------------------------------------------------
@echo.


cd /d d:/12_dev/03_visual_lisp

git status
git add .
git commit -m %hash%
git push 
goto exit


:04_PyhtonDemoDojang
@echo.
@echo -------------------------------------------------
@echo   04_PyhtonDemoDojang
@echo -------------------------------------------------
@echo.


cd /d d:/12_dev/04_PyhtonDemoDojang
git status
git add .
git commit -m %hash%
git push 
goto exit



:05_JAVA

@echo.
@echo -------------------------------------------------
@echo   05_JAVA
@echo -------------------------------------------------
@echo.


cd /d d:/12_dev/05_JAVA
git status
git add .
git commit -m %hash%
git push 

goto exit



 :06_DELPHI

@echo.
@echo -------------------------------------------------
@echo   06_DELPHI01
@echo -------------------------------------------------
@echo.


cd /d d:/12_dev/06_DELPHI01
git status
git add .
git commit -m %hash%
git push 

goto exit



:07_AutoIT

@echo.
@echo -------------------------------------------------
@echo   07_AutoIt_Script
@echo -------------------------------------------------
@echo.


cd /d d:/12_dev/07_AutoIt_Script
git status
git add .
git commit -m %hash%
git push 

goto exit



:allpush

@echo.
@echo -------------------------------------------------
@echo   d:/12_dev/01_Linux
@echo -------------------------------------------------
@echo.


cd /d d:/12_dev/01_Linux
git status
git add .
git commit -m %hash%
git push 



@echo.
@echo -------------------------------------------------
@echo   02_Excel
@echo -------------------------------------------------
@echo.

cd /d d:/12_dev/02_Excel

git status
git add .
git commit -m %hash%
git push 
goto exit

:02_Excel2

@echo.
@echo -------------------------------------------------
@echo   02_Excel2
@echo -------------------------------------------------
@echo.

cd /d d:/12_dev/02_Excel2

git status
git add .
git commit -m %hash%
git push


@echo.
@echo -------------------------------------------------
@echo   d:/12_dev/03_visual_lisp 
@echo -------------------------------------------------
@echo.


cd /d d:/12_dev/03_visual_lisp
git status
git add .
git commit  -m %hash%
git push 



@echo.
@echo -------------------------------------------------
@echo   d:/12_dev/04_PyhtonDemoDojang 
@echo -------------------------------------------------
@echo.

cd /d d:/12_dev/04_PyhtonDemoDojang
git status
git add .
git commit  -m %hash%
git push 


@echo.
@echo -------------------------------------------------
@echo   d:/12_dev/05_JAVA
@echo -------------------------------------------------
@echo.


cd /d d:/12_dev/05_JAVA
git status
git add .
git commit  -m %hash%
git push 


:exit


