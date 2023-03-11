import sys

def remove_crlf(input_filename, output_filename):
    # Open input file for reading and output file for writing
    with open(input_filename, "r") as input_file, open(output_filename, "w") as output_file:
        # Remove all CR and LF characters from the input file
        content = input_file.read().replace("\r", "").replace("\n", "")
        # Write the modified content to the output file
        output_file.write(content)

# Get the input and output filenames from the command line arguments
if len(sys.argv) > 1:
    input_filename = sys.argv[1]
else:
    print("Error: Please provide an input filename.")
    sys.exit(1)

if len(sys.argv) > 2:
    output_filename = sys.argv[2]
else:
    output_filename = "result.out"

# Call the remove_crlf function with the input and output filenames
remove_crlf(input_filename, output_filename)
