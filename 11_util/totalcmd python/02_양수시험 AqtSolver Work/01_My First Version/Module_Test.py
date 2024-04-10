def replace_comma_to_dot(_text) -> str:
    if ',' in _text:
        _text = _text.replace(',', '.')
    if ' ' in _text and not ('m' in _text):
        _text = _text.replace(' ', '.')

    if _text.count(".") >= 2:
        cleaned_number = _text.replace(".", "")
        formatted_number = "0." + cleaned_number[1:]

    else:
        formatted_number = _text

    # print('after :', text)
    return formatted_number


def move_decimal(num_str):
    if len(num_str) == 1:
        return "0." + num_str

    return num_str[:1] + '.' + num_str[1:]



print(replace_comma_to_dot("0, 1065"))
print(move_decimal("12345"))  # Output: 1.2345
print(move_decimal("123"))  # Output: 1.23
print(move_decimal("1234"))  # Output: 1.234
