; AutoHotkey v2 script to delete all .bak, .log, and .dwl files in the current directory

#Requires AutoHotkey v2.0
#SingleInstance


Loop Files, "*.bak", "FD" ; F: Files, D: Directories
{
    FileDelete A_LoopFileFullPath
}

Loop Files, "*.log", "FD"
{
    FileDelete A_LoopFileFullPath
}

Loop Files, "*.dwl", "FD"
{
    FileDelete A_LoopFileFullPath
}


