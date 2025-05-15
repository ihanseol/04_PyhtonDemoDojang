def handle_503_76():
    """
    This function demonstrates how to work with the number 503.76 in Python.
    """
    my_number = 503.76

    # Print the number
    print(f"The number is: {my_number}")

    # You can perform various operations with this number, such as:

    # 1. Rounding:
    rounded_up = round(my_number)  # 504
    rounded_down = int(my_number)  # 503
    rounded_to_one_decimal = round(my_number, 1)  # Rounds to 1 decimal place #503.8
    print(f"Rounded up: {rounded_up}")
    print(f"Rounded down: {rounded_down}")
    print(f"Rounded to 1 decimal place: {rounded_to_one_decimal}")

    # 2. Basic arithmetic:
    addition = my_number + 10
    subtraction = my_number - 5
    multiplication = my_number * 2
    division = my_number / 3
    print(f"Addition: {addition}")
    print(f"Subtraction: {subtraction}")
    print(f"Multiplication: {multiplication}")
    print(f"Division: {division}")

    # 3. String formatting (already used above):
    formatted_string = f"The result is: {my_number:.2f}"  # Format to 2 decimal places
    print(formatted_string)

    # 4. check the type
    print(f"Type of variable: {type(my_number)}")  # float

    # 5.  You can convert it to an integer, but you will lose the decimal part.
    integer_version = int(my_number)
    print(f"Integer version: {integer_version}")


if __name__ == "__main__":
    handle_503_76()
