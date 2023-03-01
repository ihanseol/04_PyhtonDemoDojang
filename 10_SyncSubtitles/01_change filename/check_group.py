# import re


# # [Sokudo] Psycho-Pass 01 [1080p BD][AV1][dual audio].mkv
# # example input string

# input_string = "[Sokudo] Psycho-Pass 01 [1080p BD][AV1][dual audio].mkv"

# # compile a regular expression pattern to match all groups
# pattern = re.compile(r'\[(\[[^\]]*\]|[^\[\]]*)*\]|(\[?[^\[\]]+\]?)')

# # find all matches of the pattern in the input string and extract the captured groups
# matches = re.findall(pattern, input_string)

# # extract the groups and print them to the console
# groups = [m[0] or m[1] for m in matches]
# print(groups)



import re
input_string = "[Sokudo] Psycho-Pass 01 [1080p BD][AV1][dual audio].mkv"
pattern = re.compile(r'(\[?[^\[\]]+\]?)')

matches = re.findall(pattern, input_string)

len_list = len(matches)

for i in range(0, len_list-1):
	print(matches[i])




# print the extracted groups
# print(matches)


