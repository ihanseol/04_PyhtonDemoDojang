#Requires AutoHotkey v1.0
#SingleInstance


IpCheck()
{
    URLDownloadToFile,http://ipinfo.io/ip, %A_ScriptDir%\showip.txt
    if ErrorLevel = 1
    {
        MsgBox, 16,IpAddresses,Your public Ipaddress could not be detected.
    }
    FileReadLINE,Mainip,%A_ScriptDir%\showip.txt, 1
    MsgBox, 64,Ipaddresses,Your Public IpAddress is: [ %Mainip% ]`n`nYour private ipAddress is: [ %A_IPAddress1% ]
    ;~ FileDelete, showip.txt
}


IpCheck()







