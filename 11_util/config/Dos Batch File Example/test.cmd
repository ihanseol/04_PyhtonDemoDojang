

@echo off


SET CMD=%~1

IF "%CMD%" == "" (
  GOTO exit
)


if "%CMD%" == "main" (
	goto main
) else (
	goto pass
)

:main
echo main
goto exit


:pass
echo pass

:exit






