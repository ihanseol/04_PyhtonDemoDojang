# Basic usage of divmod()
# divmod(a, b) returns a tuple (quotient, remainder) of a divided by b

# Example 1: Simple integer division
result = divmod(13, 5)
print(f"divmod(13, 5) = {result}")  # Output: (2, 3) because 13 ÷ 5 = 2 remainder 3

# Example 2: With larger numbers
result = divmod(100, 7)
print(f"divmod(100, 7) = {result}")  # Output: (14, 2) because 100 ÷ 7 = 14 remainder 2

# Example 3: With negative numbers
result = divmod(-13, 5)
print(f"divmod(-13, 5) = {result}")  # Output: (-3, 2)

# Example 4: With floating point numbers
result = divmod(13.5, 2.5)
print(f"divmod(13.5, 2.5) = {result}")  # Output: (5.0, 1.0)

# Example 5: Practical use - converting seconds to minutes and seconds
total_seconds = 125
minutes, seconds = divmod(total_seconds, 60)
print(f"{total_seconds} seconds = {minutes} minutes and {seconds} seconds")

# Example 6: Practical use - converting to hours, minutes, seconds
total_seconds = 3725
hours, remainder = divmod(total_seconds, 3600)
minutes, seconds = divmod(remainder, 60)
print(f"{total_seconds} seconds = {hours} hours, {minutes} minutes, {seconds} seconds")

# Example 7: Practical use - calculating digits
num = 12345
while num > 0:
    num, digit = divmod(num, 10)
    print(f"Digit: {digit}")  # Prints each digit from right to left