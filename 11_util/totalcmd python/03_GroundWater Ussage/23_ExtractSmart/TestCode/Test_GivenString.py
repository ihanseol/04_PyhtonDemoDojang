def get_editor_name(given_string):
    parts = given_string.split('\\')
    print(parts)

    return parts[0]

# Given string from the user's request
given_string = "25_Editor\\01_EmEditor\\AppData\\Config\\Bat"

# Call the function to get the desired substring
result = get_editor_name(given_string)

# Print the result to the console
print(f"The extracted string is: {result}")



