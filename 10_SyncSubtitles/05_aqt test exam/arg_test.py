import argparse

parser = argparse.ArgumentParser(description="This script does something")

# Add positional arguments
parser.add_argument("filename", help="Name of the input file")
parser.add_argument("n", type=int, help="Number of lines to read")

# Add optional arguments
parser.add_argument("-f", "--format", choices=["csv", "txt"], default="txt", help="Format of the input file")
parser.add_argument("-a", "--append", action="store_true", help="Append to the output file instead of overwriting it")
parser.add_argument("-g", "--generate", type=int, help="Generate a random number")

# Add a help message
parser.add_argument("--display-help", action="help", help="Show this help message and exit")


args = parser.parse_args()

# Print the values of the arguments
print("Filename:", args.filename)
print("Number of lines:", args.n)
print("Format of the input file:", args.format)
print("Append to the output file:", args.append)
print("Generated number:", args.generate)


