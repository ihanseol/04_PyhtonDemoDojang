import sys

# Print the number of arguments (including the script name)
print(f"Number of arguments: {len(sys.argv)}")

# Print the script name
print(f"Script name: {sys.argv[0]}")

# Print all arguments one by one
for i, arg in enumerate(sys.argv[1:], start=1):
    print(f"Argument {i}: {arg}")


print(f'1 : {sys.argv[1]}')
print(f'2 : {sys.argv[2]}')


_ = input("Enter")


