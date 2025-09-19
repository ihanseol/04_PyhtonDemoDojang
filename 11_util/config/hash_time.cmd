@echo off
:: Get the current timestamp and save it to a file
for /f "tokens=*" %%t in ('powershell -command "Get-Date -Format 'yyyyMMddHHmmss'"') do set timestamp=%%t
echo %timestamp% > timestamp.txt

:: Generate MD5 hash and extract only the hash value
for /f "skip=1 tokens=1" %%h in ('certutil -hashfile timestamp.txt MD5 ^| findstr /v "hash CertUtil"') do set hash=%%h

:: Display the hash
echo MD5 Hash: %hash%

pause