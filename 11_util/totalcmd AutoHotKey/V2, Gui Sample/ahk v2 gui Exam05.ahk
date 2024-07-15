#Requires AutoHotkey v2.0
#SingleInstance Force

saveToTxtOnSubmit:=true

othergui := Gui()
othergui.Title := "A Gui Window"
othergui.SetFont("s12")
otherguiText1 := othergui.AddText("x25 y10 w350 h60")
otherguiText2 := othergui.AddText("x50 y80 w350 h20")
otherguiText3 := othergui.AddText("x50 y110 w350 h60")
otherguiText4 := othergui.AddText("x50 y170 w350 h50")
otherguiText5 := othergui.AddText("x50 y225 w350 h100")
othergui.Show("x" A_ScreenHeight*.5 " y" A_ScreenHeight*.5 " w400 h400")
othergui.OnEvent("Close", (*) => ExitApp())
OGWindow := othergui.Hwnd

otherguiText1.text:= "Move this gui around and then hit Enter once you have moved it to the position you want the new gui to open at and see what happens"
othergui.SetFont("s8")
KeyWait("Enter", "D")

goo := Gui()          ;Window for the user to add items
goo.SetFont("s7")
Tab := goo.Add("Tab3", "x0 y-8 w294 h249 +Bottom", ["Tab1", "Tab2", "Tab3", "Tab4"])
Tab.UseTab(1) ;Tab 1 Positioning & Callers
;goo.Add('Picture', 'x0 y0 w293 h240', A_ScriptDir '\resources\images\image.png') ;optional background picture
goo.Add("Text", "x40 y8 w223 h23 +0x200", "Add an item to the thing")
goo.Add("Text", "x24 y48 w120 h23 +0x200", "Item:")
goo.Add("Text", "x24 y88 w120 h23 +0x200", "Choice")
goo.Add("Text", "x24 y128 w120 h23 +0x200", "Type")
Edit1 := goo.Add("Edit", "x160 y48 w115 h21 Number")
DDL_Choice := goo.Add("DropDownList", "x160 y88 w120 Choose1", ["Select", "Choice1", "Choice2", "Choice3", "Choice4"])
DDL_Type := goo.Add("DropDownList", "x160 y128 w120 Choose1", ["Type1", "Type2"]).OnEvent("Change", DDL_Type_Handler)
ExitBtn := goo.Add("Button", "x176 y190 w67 h23", "&Exit").OnEvent('Click', (*) => goo.Destroy())
Checkbox := goo.Add("CheckBox", "x50 y162 w250 h23 -Checked", "Save info to file").OnEvent("Click", CB_Event_Handler)
SubmitBtn1 := goo.Add("Button", "x56 y190 w66 h23 Default", "&Submit").OnEvent("Click", Tab1_Submit_Handler)

Tab.UseTab(2) ;Tab 2 Positioning & Callers
goo.SetFont("s8")
goo.Add("Text", "x16 y8 w269 h23 +0x200", "Select a choice")
goo.Add("Text", "x24 y56 w112 h23 +0x200", "Choice")
DDL_Option := goo.Add("DropDownList", "x152 y56 w120 Choose1", ["Any", "Choice1", "Choice2", "Choice3", "Choice4"]).OnEvent("Change", DDL_Type_Handler)
goo.Add("Text", "x24 y112 w112 h23 +0x200", "Area")
DDL_Area := goo.Add("DropDownList", "x152 y112 w120 Choose1", ["Any", "Area 6", "Area 5", "Area 4", "Area 3", "Area 2", "Area 1"]).OnEvent("Change", DDL_Area_Handler)
SubmitBtn2 := goo.Add("Button", "x109 y171 w80 h23", "S&ubmit").OnEvent("Click", Tab2_Submit_Handler)

Tab.UseTab(3) ;Tab 3 Positioning & Callers
goo.SetFont("s9")
goo.Add("Text", "x16 y8 w269 h45", "# of times (less than 5): ")
goo.Add("Text", "x24 y54 w112 h40", "Number")
Num := goo.Add("Edit", "x182 y56 w90")
goo.Add("Text", "x24 y105 w112 h23", "Type")
Choices := goo.Add("DropDownList", "x152 y105 w120 Choose1", ["Select One", "Choice1", "Choice2", "Choice3"]).OnEvent("Change", Choices_Handler)
SubmitBtn3 := goo.Add("Button", "x109 y180 w80 h23", "Submi&t").OnEvent("Click", Tab3_Submit_Handler)
Warn := goo.Add("Text", "x35 y142 w220 h25 +Hidden", "") ;This is a text field with a warning that appears only when the user selects choice 4

Tab.UseTab(4) ;Tab 4 Positioning & Callers
goo.SetFont("s10")
goo.Add("Text", "x24 y8 w251 h34 +0x200 +Center", "Add items by group")
MultiEditLabel := goo.Add("Text", "x17 y65 w125 h130 +Wrap", "Insert the items you want to include`nOnly one item per line.")
MultiEdit := goo.Add("Edit", "x152 y48 w130 h136 +Multi +0x1000 +0x4000"
, "This text appears in the edit field of the Gui before the user types/pastes any information")
;gAddLocus.Add("Text", "x136 y48 w2 h140 +0x1 +0x10")
ColorLabel := goo.Add("Text", "x30 y170", "Choose a color:")
DDL_group_color := goo.Add("DropDownList", "x45 y190 w75 Choose1", ["Black", "Yellow", "Grey", "Green", "Blue"])
ButtonSubmit4 := goo.Add("Button", "x176 y190 w80 h23 +Center", "&Submit").OnEvent("Click", Tab4_Submit_Handler)

;Tab 1 Event Handlers
Tab1_Submit_Handler(*){
    WinActivate(OGWindow)
    if DDL_Choice.text = "Select"{
        MsgBox("You must choose an option")
    }
    else if DDL_Choice.text != "Select"{
        UserFunction(DDL_Choice.text, DDL_Type.text, Edit1.value)
    }
    Edit1.Value := ""
}
CB_Event_Handler(*){
    if Checkbox.value = 1
        saveToTxtOnSubmit := true
    else
        saveToTxtOnSubmit := false
}

;Tab 2 Event Handlers
DDL_Type_Handler(*){
    ;MsgBox(You changed the type value to DDL_Type.value)
}
DDL_Area_Handler(*){
    ;MsgBox(You changed the area value to DDL_Area.value)
}
Tab2_Submit_Handler(*){
    WinActivate(OGWindow)
    if DDL_Option.text = "Any" and DDL_Area.text = "Any"{
        MsgBox("You arent allowed to not select options from the drop down menus")
    }
    else if DDL_Option.text = "Any" || DDL_Area.text = "Any"{
        MsgBox("You must pick an option in each drop down")
    }
    else if DDL_Option.text != "Any" and DDL_Area.text != "Any"{  ;this could just be an else statement because this will always evaluate to true if the script gets to this point
        otherguiText2.text:= "You selected " DDL_Area.text " and " DDL_Option.text
    }


}
;Tab 3 Event Handlers
Choices_Handler(*){
    if Choices.text = "Choice3"{
        Tab.UseTab(3)
        goo.SetFont("s7")
        Warn.text:= "Warning! Choosing this selection is dangerous for some reason."
        Warn.Opt("-Hidden")
        otherguiText3.SetFont("cRed")
    }
    if Choices.text != "Choice3"{
        Warn.text:= ""
        Warn.Opt("+Hidden")
        otherguiText3.SetFont("c000000")
    }
}
Tab3_Submit_Handler(*){
    if Choices.value = "1" {
        MsgBox("You must choose an option before submitting.")
        return
    }
    WinActivate(OGWindow)
    name := Choices.text
    iterations := 1
    while iterations <= Num.value {
        MsgBox(name)
        if A_Index = 5
            break
        iterations+= 1
    }
    otherguiText3.text:= "You displayed a msgbox of " Choices.text A_Space Num.text "times"
    if Choices.text="Choice3"{
        Choices.Delete(4)
        MsgBox("You were warned, you rascal."
        . "`n`n" "The 'Choice3' option has now been removed"
        . "`n`n" . "If you need to enable this functionality please see your system administrator")
    }
}

;Tab 4 Event Handlers
Tab4_Submit_Handler(*){
    MsgBox("You have clicked submit on tab 4. I wonder what it does...")
    otherguiText1.text:=""
    otherguiText2.text:=""
    otherguiText3.text:=""
    otherguiText4.text:="We have reset all of your previous entries, and this text will disappear in 3.5 seconds"
    otherguiText5.text:=MultiEdit.Text
    otherguiText5.SetFont("c" DDL_group_color.text)
    SetTimer((*) => otherguiText4.text:="", -3500)
}

;Menu wide options
Tab.UseTab() ;On showing gui, begin with tab 1
goo.OnEvent('Close', (*) => goo.Destroy()) ;when closing the gui, destroy the gui
goo.Title := "My GUI with 4 tabs"
goo.x_pos := mid_pos(othergui).get("w")
goo.y_pos := mid_pos(othergui).get("h")
goo.width := 300
goo.height := 240
goo.Show("w " goo.width " h" goo.height " x" mid_pos(othergui).get("x")-goo.x_pos/2-goo.width-1 " y" mid_pos(othergui).get("y")-goo.y_pos/2)

;Defined Function
UserFunction(Choice, TheType, EditBox){

    string1 := "You chose " Choice " and then you selected your type to be " TheType " for item #: " EditBox
    if (Checkbox.value = 1){
        FileAppend(string1, "myFile.txt")
        MsgBox("The text has been saved to a file named MyFile.txt in " A_ScriptDir)
    }
    else{
        MsgBox("You chose not to save this text to a file: "
    . "`n" string1)
    }
}

;Gui function for gui positioning
mid_pos(gui){
    CoordMode("Menu", "Screen")
    gui.getPos(&x, &y, &w, &h)
    gui_Pos := Map()
    gui_Pos.set("x", x+w/2)
    gui_Pos.set("y", y+h/2)
    gui_Pos.set("w", w)
    gui_Pos.set("h", h)
    return gui_Pos
}

Esc::ExitApp()