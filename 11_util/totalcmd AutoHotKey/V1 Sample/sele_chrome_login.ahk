#sele_chrome_login.ahk

#SingleInstance force
Gui, Add, Text, x30 y20 w350 h20, Select your browser
Gui, Add, Radio, x30 y40 w60 h20 vR1 checked, Chrome
Gui, Add, Radio, x100 y40 w60 h20 vR2 , FireFox
Gui, Add, Radio, x170 y40 w60 h20 vR3 , Opera
Gui, Add, Radio, x240 y40 w60 h20 vR4 , IE

Gui, Add, Text, x30 y100 w120 h20,Login Site
Gui, Add, Edit, x160 y100 w200 h20 vSiteUrl, https://www.gseek.kr/member/rl/login/loginForm.do  ;

Gui, Add, Text, x30 y120 w120 h20 , ID
Gui, Add, Edit, x160 y120 w200 h20 vID, xxxx@yyy.com  ;

Gui, Add, Text, x30 y140 w120 h20, Password
Gui, Add, Edit, x160 y140 w200 h20 vPassword, abcde~!@  ;

Gui, Add, Button, x220 y170 w200 h20, Login ;

Gui, Show , ,Site Login

CoordMode, Mouse, Screen
SetKeyDelay, -1, -1
return


ButtonLogin:
{
	global SiteUrl, R1, R2, R3, ID, Password
	Gui, Submit, nohide

	if R1 = 1
		browser := "Selenium.ChromeDriver"
	else if R2 = 1
		browser := "Selenium.FirefoxDriver"
	else if R3 = 1
		browser := "Selenium.OperaDriver"
	else if R4 = 1
		browser := "Selenium.IEDriver"
	else 
		browser := "Selenium.ChromeDriver"
	driver := ComObjCreate(browser)
	driver.Get(SiteUrl)

	driver.findElementsByName("memberNo").item[1].SendKeys(ID)
	driver.findElementsByName("password").item[1].SendKeys(Password)
;	driver.findElementsById("password").item[1].SendKeys(Password)
	driver.FindElementByClass("btn_button").Click

	MsgBox login complete
}
return


ButtonEnd:
{
	ExitApp
}
return

#IfWinActive ahk_class AutoHotkeyGUI
ESC::goto, ButtonEnd
return
#IfWinActive
