@echo off
REM No escaping required, if delayed expansion is disabled
set test1=Test1!

setlocal EnableDelayedExpansion
REM One caret required
REM Delayed expansion uses carets independent of quotes to escape the exclamation mark
set "test2=Test2^!"

REM Two carets required
REM The first caret escapes the second caret in phase2 of the parser
REM Later in the delayed expansion phase, the remaining caret escapes the exclamation mark
set test3=Test3^^!


echo !test1!
echo !test2!
echo !test3!

