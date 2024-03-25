import os
import re


# data
# [Sokudo] Psycho-Pass 01 [1080p BD][AV1][dual audio].mkv


# get a list of all .mkv files in the current directory
files = [f for f in os.listdir() if f.endswith('.mkv')]

# compile a regular expression pattern to match the file name
#pattern = re.compile(r'\[(\w+)\] (.+) \[(\d+p BD)\]\[(\w+)\]\[(\w+ audio)\]\.mkv')
#pattern = re.compile(r'\[Sokudo\] (.+) \[(\d+p BD)\]\[(\w+)\]\[dual audio\]\.mkv')

pattern = re.compile(r'(\[[^\]]*\]|[^\[\]]*)')



# loop through the files and extract the file name
# for file in files:
#     # match the pattern against the file name
#     match = pattern.match(file)
#     if match:
#         # extract the relevant parts of the file name
#         show_name = match.group(2)
#         episode_num = match.group(3).split(' ')[0]
#         file_name = f"{show_name} {episode_num}.mkv"
#         print(file_name)




# loop through the files and extract the file name
for file in files:
    # match the pattern against the file name
    match = pattern.match(file)
    if match:
        # extract the relevant parts of the file name
        a = match.group(1)
        b = match.group(2)
        c = match.group(3)
        d = match.group(4)
        # e = match.group(5)

        
        print(f" a : {a}")
        print(f" b : {b}")
        print(f" c : {c}")
        print(f" d : {d}")
        # print(f" e : {d}")

        print("--------------------")
        
