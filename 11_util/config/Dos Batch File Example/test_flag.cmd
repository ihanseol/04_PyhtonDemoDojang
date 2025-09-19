@echo off


SET IGNORE_GIT=0


if %IGNORE_GIT%==0 (
          goto jump_ignore_no
) else (
	   goto jump_ignore_yes
)





:jump_ignore_no
echo jump_ignore_no
goto exit


:jump_ignore_yes
echo jump_ignore_yes


:exit







