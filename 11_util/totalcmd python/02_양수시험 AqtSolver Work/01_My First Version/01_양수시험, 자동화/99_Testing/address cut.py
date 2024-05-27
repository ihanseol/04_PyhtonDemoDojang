




# # input_str = "세종시 전의면 유천리 227번지"
#
# # input_str = "충청남도 보령시 주교면 은포리 산8-1번지"
#
# input_str = "대전시 유성구 장대동 278-13"
#
# # Split the input string by spaces
# parts = input_str.split()
#
# print(parts)
#
# i = 0
# for part in parts:
#     if (part[-1:] == "면") or (part[-1:] == "구"):
#         break
#     i = i + 1
#
#
#
#     # Select the parts you want to keep
# result = ' '.join(parts[i:])
# print(result)


# Input strings
input_str1 = "세종시 전의면 유천리 227번지"
input_str2 = "충청남도 보령시 주교면 은포리 산8-1번지"
input_str3 = "대전시 유성구 장대동 278-13"


# Function to process the input string
def process_address(input_str):
    # Split the input string by spaces
    parts = input_str.split()

    print(parts)  # For debugging

    # Initialize the index
    i = 0

    # Iterate over the parts to find the target index
    for part in parts:
        if part.endswith("면") or part.endswith("구"):
            break
        i += 1

    # Select the parts you want to keep
    result = ' '.join(parts[i:])
    return result


# Process each input string
result1 = process_address(input_str1)
result2 = process_address(input_str2)
result3 = process_address(input_str3)

print(result1)  # 전의면 유천리 227번지
print(result2)  # 주교면 은포리 산8-1번지
print(result3)  # 유성구 장대동 278-13


