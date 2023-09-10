import random
import string
import pyperclip

def generate_random_string(length):
  """Generate a random string of the specified length."""
  characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_" + "-" + "!@#$%^&*"
  return ''.join(random.choice(characters) for _ in range(length))

def copy_to_clipboard(text):
  """Copy the specified text to the clipboard."""
  pyperclip.copy(text)

def main():
  # Get the length of the random string to generate.
  length = int(input("Enter the length of the random string: "))

  # Generate the random string.
  random_string = generate_random_string(length)

  # Print the random string.
  print("The random string is:", random_string)

  # Copy the random string to the clipboard.
  copy_to_clipboard(random_string)

if __name__ == "__main__":
  main()
