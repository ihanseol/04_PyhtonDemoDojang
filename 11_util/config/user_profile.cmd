
@echo off

set "GITT=C:\Program Files\Git\usr\bin\"
set "TCOMMANDER=c:\Program Files\totalcmd\ini\config\"
set "TC=c:\Program Files\totalcmd\"

set "VII=c:\Program Files\Vim\vim91\"
set "CODE=c:\Users\minhwasoo\AppData\Local\Programs\Microsoft VS Code\"

set "SUBLIMETEXT=c:\Program Files\Sublime Text\"
set "SUBLIME32=c:\Program Files\totalcmd\RunAsTool\Editor\SublimeText\"

set "FZFP=c:\Users\minhwasoo\.fzf\bin\"
set "FARMANAGER=c:\Program Files\Far Manager\"

set "ME=c:\Users\minhwasoo\Desktop\"
set "PYTHON_APP=c:\Program Files\totalcmd\ini\02_python\"
set "POPL=c:\ProgramData\35_ETC\poppler-23.01.0\Library\bin\"

set "GHISLER=c:\Users\minhwasoo\AppData\Roaming\GHISLER\"
set "TCCONFIG=c:\Users\minhwasoo\AppData\Roaming\GHISLER\CONFIG\"



:: subl "c:\Program Files\totalcmd\ini\config\my_python_module_install.cmd"

:: FDEV - Folder Dev
set "FDEV=d:\12_dev\"


set EDITOR=subl32
:: set EDITOR=gvim
:: set EDITOR=code
:: set EDITOR=subl

set PATH=%PATH%;%GITT%;%TCOMMANDER%;%ME%;%VII%;%SUBLIMETEXT%;%SUBLIME32%;%FZFP%;%FARMANAGER%;%PYTHON_APP%;%POPL%;%GHISLER%;%TCCONFIG%;


doskey /macrofile="%TCOMMANDER%\user_aliases.cmd" 

