@ECHO OFF
SETLOCAL
REM FooBar parameter demo
REM By Garret Wilson

SET CMD=%~1

IF "%CMD%" == "" (
  GOTO usage
)
SET FOO=
SET DEFAULT_FOO=default
SET BAR=
SET BAZ=

SHIFT
:args
SET PARAM=%~1
SET ARG=%~2
IF "%PARAM%" == "--foo" (
  SHIFT
  IF NOT "%ARG%" == "" (
    IF NOT "%ARG:~0,2%" == "--" (
      SET FOO=%ARG%
      SHIFT
    ) ELSE (
      SET FOO=%DEFAULT_FOO%
    )
  ) ELSE (
    SET FOO=%DEFAULT_FOO%
  )
) ELSE IF "%PARAM%" == "--bar" (
  SHIFT
  IF NOT "%ARG%" == "" (
    SET BAR=%ARG%
    SHIFT
  ) ELSE (
    ECHO Missing bar value. 1>&2
    ECHO:
    GOTO usage
  )
) ELSE IF "%PARAM%" == "--baz" (
  SHIFT
  SET BAZ=true
) ELSE IF "%PARAM%" == "" (
  GOTO endargs
) ELSE (
  ECHO Unrecognized option %1. 1>&2
  ECHO:
  GOTO usage
)
GOTO args
:endargs

ECHO Command: %CMD%
IF NOT "%FOO%" == "" (
  ECHO Foo: %FOO%
)
IF NOT "%BAR%" == "" (
  ECHO Bar: %BAR%
)
IF "%BAZ%" == "true" (
  ECHO Baz
)

REM TODO do something with FOO, BAR, and/or BAZ
GOTO :eof

:usage
ECHO FooBar
ECHO Usage: foobar ^<command^> [--foo [^<fooval^>]] [--bar ^<barval^>] [--baz]
EXIT /B 1