#Requires AutoHotkey v2.0
#SingleInstance

IpCheck() {
    try {
        Download("http://ipinfo.io/ip", A_ScriptDir "\showip.txt")
        publicIp := FileRead(A_ScriptDir "\showip.txt")
        privateIp := GetLocalIP()
        MsgBox("Your Public IpAddress is: [ " publicIp " ]`n`nYour private ipAddress is: [ " privateIp " ]", "Ipaddresses", "64")
    } catch as err {
        MsgBox("Your public Ipaddress could not be detected.", "IpAddresses", "16")
    }
    FileDelete(A_ScriptDir "\showip.txt")  ; Uncomment this line if you want to delete the file
}

GetLocalIP() {
    objWMIService := ComObject("WbemScripting.SWbemLocator").ConnectServer()
    colItems := objWMIService.ExecQuery("SELECT * FROM Win32_NetworkAdapterConfiguration WHERE IPEnabled = True")
    for objItem in colItems {
        if (objItem.IPAddress[0] != "0.0.0.0")
            return objItem.IPAddress[0]
    }
    return "IP Not Found"
}








IpCheck()
