CoordMode, Pixel, Screen

;~ dual monitor image search



ImageSearch, testX, testY, -2560, 0, 2559, 1439, *32 excel_button.png
if !ErrorLevel {
	MsgBox, found1
}


SysGet, VirtualScreenWidth, 78
SysGet, VirtualScreenHeight, 79
SysGet, VirtualScreenLeft, 76
SysGet, VirtualScreenTop, 77

ImageSearch, testX, testY, VirtualScreenLeft, VirtualScreenTop, VirtualScreenLeft+VirtualScreenWidth, VirtualScreenTop+VirtualScreenHeight, *32 test.png
if !ErrorLevel {
	MsgBox, found2
}


SysGet, Mon2, Monitor, 2

ImageSearch, testX, testY, Mon2Left, Mon2Top, Mon2Right, Mon2Bottom, *32 test.png
if !ErrorLevel {
	MsgBox, found3
}

Exit