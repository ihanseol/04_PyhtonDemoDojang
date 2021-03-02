
def decorator_function(original_function):
    def wrapper_function():
        print(f'wrapper executed this before {original_function.__name__}')
        return original_function()
    return wrapper_function

@decorator_function
def display():
    print('display function ran')

# equal to  upper decorator :  display = decorator_function(display)

display()














