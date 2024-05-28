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

"""
경상남도 거창군 신원면 덕산리 산 13번지

대전시 유성구 장대동 278-13

충청남도 당진시 대덕동 1321번지
충청남도 보령시 주포면 봉당리 647 번지
충청남도 보령시 주교면 은포리 산8-1번지
세종특별자치시 부강면 금병로 1263-112 번지

충청남도 부여군 은산면 은산리 177-6 번지
충청남도 부여군 외산면 반교리 574

"""


# Input strings
input_str1 = "세종특별자치시 부강면 금병로 1263-112 번지"
input_str2 = "충청남도 보령시 주교면 은포리 산8-1번지"
input_str3 = "대전시 유성구 장대동 278-13번지"
input_str4 = "전의면 유천리 227번지aaaaaaaa"


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

    if len(result) > 21:
        if "번지" in result:
            result = input_str.replace("번지", "")

    return result


# Process each input string
result1 = process_address(input_str1)
result2 = process_address(input_str2)
result3 = process_address(input_str3)
result4 = process_address(input_str4)

print(result1, len(result1))  # 전의면 유천리 227번지
print(result2, len(result2))  # 주교면 은포리 산8-1번지
print(result3, len(result3))  # 유성구 장대동 278-13
print(result4, len(result4))  # 유성구 장대동 278-13
