import re

# Define the input string
input_string = '0001 - 0003 장윤정-목포행 완행열차.mp3'

# Use a regular expression to extract the desired output
output = re.sub(r'(\d{4}) - (\d{4})', r'\1', input_string)

# Print the output
print(output)
