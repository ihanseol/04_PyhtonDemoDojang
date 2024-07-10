#Persistent
^!t:: ; Define a hotkey (Ctrl + Alt + T) to trigger the translation process
{
    ; Step 1: Take a screenshot (You might need to adjust this depending on your setup)
    Send, {PrintScreen}
    Sleep, 500 ; Wait for the screenshot to be taken

    ; Step 2: Open Google Lens (You might need to adjust this depending on your device)
    Run, https://lens.google/
    WinWaitActive, Google Lens

    ; Step 3: Send keys to navigate to the image upload section and select the image (Adjust as needed)
    Send, {Tab}{Tab}{Enter} ; Navigate to "Import"
    Sleep, 1000 ; Wait for the upload window to open
    Send, ^v ; Paste the screenshot
    Sleep, 1000 ; Wait for the image to upload

    ; Step 4: Select translation option (Adjust as needed)
    Send, {Tab}{Tab}{Enter} ; Navigate to "Translate"
    Sleep, 2000 ; Wait for translation to complete

    ; Step 5: Copy translated text (Adjust as needed)
    Send, ^a^c ; Select all and copy translated text
    Sleep, 500 ; Wait for copying

    ; Step 6: Close Google Lens (Adjust as needed)
    Send, ^w ; Close Google Lens tab

    ; Step 7: Paste translated text wherever needed (Adjust as needed)
    Send, ^v ; Paste translated text
    Return
}
