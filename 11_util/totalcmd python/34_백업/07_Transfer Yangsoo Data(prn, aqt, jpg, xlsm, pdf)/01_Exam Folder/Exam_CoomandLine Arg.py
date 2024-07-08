import sys

# 명령줄 인수 출력
print("명령줄 인수:", sys.argv)

# 첫 번째 인수 (스크립트 이름)
script_name = sys.argv[0]
print("스크립트 이름:", script_name)

# 두 번째 인수 (첫 번째 사용자 인수)
if len(sys.argv) > 1:
    first_arg = sys.argv[1]
    print("첫 번째 사용자 인수:", first_arg)
else:
    print("사용자 인수가 없습니다.")


#
# import sys
#
# # Get the script name (including .py) from argv[0]
# script_name = sys.argv[0]
#
# # Get all arguments passed to the script (from argv[1] onwards)
# arguments = sys.argv[1:]
#
# # Print a message summarizing the script name and arguments
# print(f"Script: {script_name}")
# if arguments:
#   print(f"Arguments: {arguments}")
# else:
#   print("No arguments provided.")
#
# # Example usage with arguments
# if len(arguments) > 1 and arguments[0] == "greet":
#   name = arguments[1]
#   print(f"Hello, {name}!")



