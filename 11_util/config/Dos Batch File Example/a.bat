
@echo OFF

if [%1]==[] (
	goto changelocale
) else (
	goto power
)

:power
powercfg /change monitor-timeout-ac  %1
echo Setting %1 minutes
GOTO end

:changelocale
chcp 437
echo Locale are changed
GOTO end

:end

echo on



