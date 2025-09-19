
#! /bin/cmd


@echo off

SET CMD=%~1

IF "%CMD%" == "" (
  GOTO allpull
)

if "%CMD%" == "1" goto 01_Linux
if "%CMD%" == "2" goto 02_Excel
if "%CMD%" == "22" goto 02_Excel2
if "%CMD%" == "3" goto 03_visual_lisp
if "%CMD%" == "4" goto 04_PyhtonDemoDojang
if "%CMD%" == "5" goto 05_JAVA
if "%CMD%" == "7" goto 07_AutoIT


@echo on

:01_Linux
@echo.
@echo -------------------------------------------------
@echo   01_Linux 
@echo -------------------------------------------------
@echo.


cd /d d:/12_dev/01_Linux
git pull
exit /b


:02_Excel

@echo.
@echo -------------------------------------------------
@echo   02_Excel
@echo -------------------------------------------------
@echo.

cd /d d:/12_dev/02_Excel
git pull
exit /b


:02_Excel2

@echo.
@echo -------------------------------------------------
@echo   02_Excel2
@echo -------------------------------------------------
@echo.

cd /d d:/12_dev/02_Excel2
git pull
exit /b


:03_visual_lisp

@echo.
@echo -------------------------------------------------
@echo   03_visual_lisp
@echo -------------------------------------------------
@echo.


cd /d d:/12_dev/03_visual_lisp
git pull
exit /b


:04_PyhtonDemoDojang
@echo.
@echo -------------------------------------------------
@echo   04_PyhtonDemoDojang
@echo -------------------------------------------------
@echo.

git pull
exit /b


:05_JAVA

@echo.
@echo -------------------------------------------------
@echo   05_JAVA
@echo -------------------------------------------------
@echo.
cd /d d:/12_dev/05_JAVA
git pull
exit /b

:07_AutoIT

@echo.
@echo -------------------------------------------------
@echo   07_AutoIt_Script
@echo -------------------------------------------------
@echo.
cd /d d:/12_dev/07_AutoIt_Script
git pull
exit /b

goto exit



:allpull

@echo.
@echo -------------------------------------------------
@echo   01_Linux 
@echo -------------------------------------------------
@echo.

cd /d d:/12_dev/01_Linux
git pull


@echo.
@echo -------------------------------------------------
@echo   02_Excel
@echo -------------------------------------------------
@echo.

cd /d d:/12_dev/02_Excel
git pull

@echo.
@echo -------------------------------------------------
@echo   02_Excel2
@echo -------------------------------------------------
@echo.

cd /d d:/12_dev/02_Excel2
git pull


@echo.
@echo -------------------------------------------------
@echo   03_visual_lisp
@echo -------------------------------------------------
@echo.


cd /d d:/12_dev/03_visual_lisp
git pull


@echo.
@echo -------------------------------------------------
@echo   04_PyhtonDemoDojang
@echo -------------------------------------------------
@echo.

cd /d d:/12_dev/04_PyhtonDemoDojang
git pull


@echo.
@echo -------------------------------------------------
@echo   05_JAVA
@echo -------------------------------------------------
@echo.

cd /d d:/12_dev/05_JAVA
git pull








