import sys


def get_index(list_path):
    i = 0
    for _ in list_path:
        i += 1
        if _.endswith('\\'):
            return i


print(f"Number of arguments: {len(sys.argv)}")
print(f"Script name: {sys.argv[0]}")

list_arg = []

for i, arg in enumerate(sys.argv[1:], start=1):
    print(f"Argument {i}: {arg}")
    list_arg.append(arg)
    print(list_arg)


paths = list_arg
paths = [path if not path.endswith('\\') else path for path in paths]
i = get_index(list_arg)


source = ''.join(paths[:i])
target = ''.join(paths[i:])

# Print the results
print("Source:", source)
print("Target:", target)

# print(f'1 : {sys.argv[1]}')
# print(f'2 : {sys.argv[2]}')
# print(f'3 : {sys.argv[3]}')


_ = input("Enter")
