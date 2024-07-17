import sys

# Check if the path is provided as a command line argument
if len(sys.argv) > 1:
    # The path is the first argument after the script name
    path = sys.argv[1].strip('"')
    print(f"The path provided is: {path}")
else:
    print("No path provided.")
