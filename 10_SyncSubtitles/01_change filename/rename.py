import re
import os

# input_string = "[Sokudo] Psycho-Pass 01 [1080p BD][AV1][dual audio].mkv"
pattern = re.compile(r'(\[?[^\[\]]+\]?)')
current_dir = os.getcwd()

files = [f for f in os.listdir() if f.endswith('.mkv')]

for file_name in files:
	matches = re.findall(pattern, file)
	len_list = len(matches)

	# for i in range(0, len_list-1):
	# 	print(matches[i])

	new_filename = matches[1][1:-1]+matches[len_list-1]
	print(new_filename)
	print(os.path.join(current_dir, file_name))
	print(os.path.join(current_dir, new_filename))


	os.rename(os.path.join(current_dir, file_name), os.path.join(current_dir, new_filename))	
