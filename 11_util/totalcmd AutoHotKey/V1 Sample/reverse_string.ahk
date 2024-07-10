ReverseString(inputString) {
    reversedString := ""
    loop, parse, inputString
        reversedString := A_LoopField . reversedString
    return reversedString
}

MsgOutReversedString(inputString) {
    reversedString := ReverseString(inputString)
    loop, parse, reversedString
        MsgBox, % "Character: " A_LoopField
}

; Example usage:
originalString := "this is string"
MsgOutReversedString(originalString)
