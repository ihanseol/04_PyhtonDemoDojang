;==============================================================================
;= This file is registered via registry to auto load with each instance of cmd.
;================================ general info ================================
;= https://stackoverflow.com/a/59978163/985454  -  how to set it up?
;= https://gist.github.com/postcog/5c8c13f7f66330b493b8  -  example doskey macrofile
;========================= loading with cmd shortcut ==========================
;= create a shortcut with the following target :
;= %comspec% /k "(doskey /macrofile=%userprofile%\cmd\aliases.mac)"

alias=subl %USERPROFILE%\cmd\aliases.mac
hosts=runas /noprofile /savecred /user:QWERTY-XPS9370\administrator "subl C:\Windows\System32\drivers\etc\hosts" > NUL

p=@echo "~~ powercfg -devicequery wake_armed ~~" && powercfg -devicequery wake_armed && @echo "~~ powercfg -requests ~~ " && powercfg -requests && @echo "~~ powercfg -waketimers ~~"p && powercfg -waketimers

ls=ls --color=auto $*
ll=ls -l --color=auto $*
la=ls -la --color=auto $*
grep=grep --color $*

~=cd %USERPROFILE%
cdr=cd C:\repos
cde=cd C:\repos\esquire
cdd=cd C:\repos\dixons
cds=cd C:\repos\stekkie
cdu=cd C:\repos\uplus
cduo=cd C:\repos\uplus\oxbridge-fe
cdus=cd C:\repos\uplus\stratus

npx=npx --no-install $*
npxi=npx $*
npr=npm run $*

now=vercel $*


;=only in bash
;=alias whereget='_whereget() { A=$1; B=$2; shift 2; eval \"$(where $B | head -$A | tail -1)\" $@; }; _whereget'

history=doskey /history
;= h [SHOW | SAVE | TSAVE ]
h=IF ".$*." == ".." (echo "usage: h [ SHOW | SAVE | TSAVE ]" && doskey/history) ELSE (IF /I "$1" == "SAVE" (doskey/history $g$g %USERPROFILE%\cmd\history.log & ECHO Command history saved) ELSE (IF /I "$1" == "TSAVE" (echo **** %date% %time% **** >> %USERPROFILE%\cmd\history.log & doskey/history $g$g %USERPROFILE%\cmd\history.log & ECHO Command history saved) ELSE (IF /I "$1" == "SHOW" (type %USERPROFILE%\cmd\history.log) ELSE (doskey/history))))
loghistory=doskey /history >> %USERPROFILE%\cmd\history.log

;=exit=echo **** %date% %time% **** >> %USERPROFILE%\cmd\history.log & doskey/history $g$g %USERPROFILE%\cmd\history.log & ECHO Command history saved, exiting & timeout 1 & exit $*
exit=echo **** %date% %time% **** >> %USERPROFILE%\cmd\history.log & doskey/history $g$g %USERPROFILE%\cmd\history.log & exit $*

;============================= :end ============================
;= rem ******************************************************************
;= rem * EOF - Don't remove the following line.  It clears out the ';'
;= rem * macro. We're using it because there is no support for comments
;= rem * in a DOSKEY macro file.
;= rem ******************************************************************
;=