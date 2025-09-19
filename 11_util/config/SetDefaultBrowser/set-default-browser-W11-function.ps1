  function Set-browser {
  	[cmdletbinding()]
	Param([string]$browser)

	  # Changeing default browser for Windows 11 only #
	  if ($env:OS -ne 'Windows_NT') { throw 'This script runs on Windows only' }
	  Stop-Process -ErrorAction Ignore -Name SystemSettings
	  Start-Process ms-settings:defaultapps
	  $ps = Get-Process -ErrorAction Stop SystemSettings
	  do {
	    Start-Sleep -Milliseconds 100
	    $ps.Refresh()
	  } while ([int] $ps.MainWindowHandle)
	  Start-Sleep -Milliseconds 200
	  # Entering key strokes mode.
	  $shell = New-Object -ComObject WScript.Shell
	  # Tab to the "Set defaults for applications".
	  foreach ($i in 1..4) { $shell.SendKeys('{TAB}'); Start-Sleep -milliseconds 100 }
	  #
	  # Set Chrom as a defaults browser
	  #$shell.SendKeys("chrom"); Start-Sleep -seconds 1
	  #
	  # Set Firefox as a defaults browser
	  #$shell.SendKeys("firefox"); Start-Sleep -seconds 1
	  #
	  # Set EDGE as a defaults browser
	  #$shell.SendKeys("edge"); Start-Sleep -seconds 1
	  $shell.SendKeys("$browser"); Start-Sleep -seconds 1
	  #
	  $shell.SendKeys('{TAB}'); Start-Sleep -milliseconds 100
	  $shell.SendKeys('{ENTER}'); Start-Sleep -milliseconds 100
	  $shell.SendKeys('{ENTER}'); Start-Sleep -milliseconds 100
	  $shell.SendKeys('%{F4}')
	  # Check that the browser was changed
	  Start-Process "https://www.microsoft.com"
  }

Set-ExecutionPolicy -ExecutionPolicy AllSigned
Set-browser edge
