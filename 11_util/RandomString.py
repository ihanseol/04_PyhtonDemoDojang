import random
import string
import pyperclip
from pick import pick


def input_length():
  
  try:    
    # Get the length of the random string to generate.
    length = int(input("Enter the length of the random string: "))
      
  except ValueError:
    print(' value error so length is set to default : 13')    
    length = 13

  return length



def generate_random_string(length, choice):
  """Generate a random string of the specified length."""
  if choice == 0:
    characters = string.ascii_lowercase + string.digits  + string.ascii_uppercase 
  else:
    characters = string.ascii_lowercase + string.digits  + string.ascii_uppercase  + "*_-@!^#*$^%^#&-_*@"

  return ''.join(random.choice(characters) for _ in range(length))

def copy_to_clipboard(text):
  """Copy the specified text to the clipboard."""
  pyperclip.copy(text)


def main():   
    title = 'Please choose your Normal and Special characters: '
    options = ['Normal Characters', 'Special Characters']
    option, index = pick(options, title, indicator='=>', default_index=1)

  
    print('----------------------------------------------------------------')
  
    if index == 0:
      print('Generate Random String by Normal Characters ...')
    else:
      print('Generate Random String by Special Characters ...')
    
    print('----------------------------------------------------------------')
    
    length = input_length()

    # Generate the random string.
    random_string = generate_random_string(length, index)


    # Print the random string.
    print("The random string is:", random_string)

    # Copy the random string to the clipboard.
    copy_to_clipboard(random_string)

    print('----------------------------------------------------------------')


if __name__ == "__main__":
  main()


