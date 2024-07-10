

F8::

MsgBox % "OS :" . getOSVersion() . "`n" .  "CPU: " .  getCpuName()  . "`n" .  "Memory: " . getTotalPhysicalMemory( ) .  "`n" . "Disk: " . getDisk()
;~ MsgBox % "OS :" . getOSVersion()
return


getOSVersion() {

	RegRead, osVersion, HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion, ProductName
	return osVersion
}

getCpuName() {

	RegRead, cpuName, HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System\CentralProcessor\0, ProcessorNameString
	return cpuName
}


getTotalPhysicalMemory() {

	totalMemory := ComObjGet("winmgmts:").ExecQuery("SELECT * FROM Win32_ComputerSystem").ItemIndex(0).TotalPhysicalMemory
	return Round(totalMemory / 1024 / 1024 / 1024) . " GB"

}


getDisk() {

		DriveSpaceFree, free, C:\
		return Round(free / 1024) . " GB"

}


