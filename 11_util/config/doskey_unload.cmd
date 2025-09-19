@echo off

for /F "delims==" %%M in ('doskey /macros') do (
    doskey %%M=
)

doskey reloadall="%TCOMMANDER%"\doskey_setting.cmd
doskey resource="%TCOMMANDER%"\doskey_setting.cmd

exit /b