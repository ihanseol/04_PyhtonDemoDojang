/*
*************************************************************************
* This script saves X and Y coordiates in a file when you click         *
* It is very useful for quickly determining posotions on the screen     *
* o rto record several x - y position to be parsed later on by          *
* a macro whoch would click those positions automatically               *
*                                                                       *
* Use the Right Mouse button or Esc to exit th application.             *
*************************************************************************
*/


oldClip := clipboardAll
clipboard := ""

Loop
{

	MouseGetPos, X, Y
	ToolTip, % "x:" X ",  y:" Y
	Sleep 10

}

ESC::
RButton::
	;clipboard := oldClip
	ExitApp
~LButton::clipboard .= "Click " X ", " Y "`n"



