import re

# given = "y:\13_ExaVideo\03_Animation 메카, 로봇\Argevollen S01 1080p BDRip 10 bits DD x265-EMBER\S01E02-Awakening [79EA1F4B].mkv"
given = "y:\13_ExaVideo\03_Animation 메카, 로봇\Argevollen S01 1080p BDRip 10 bits DD x265-EMBER\S01E03-One Man Army [3ZDA3az288C].mkv"

pattern = r"\[([0-9A-Za-z]+)\]"
match = re.search(pattern, given)

if match:
    selected_text = match.group(0)  # To get the brackets as well
    selected_text_1 = match.group(1) # To get only the hexadecimal value
    print(selected_text)
    print(selected_text_1)
else:
    print("Pattern not found")



