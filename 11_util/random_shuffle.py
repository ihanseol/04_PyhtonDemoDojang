import random

string = "abcdefghijklmnopqrstuvwxyz"

# Make a list of characters from the string
chars = list(string)

# Shuffle the list
random.shuffle(chars)

# Convert shuffled list back to string
shuffled_string = ''.join(chars)

print(shuffled_string)
print(''.join(sorted(shuffled_string)))



