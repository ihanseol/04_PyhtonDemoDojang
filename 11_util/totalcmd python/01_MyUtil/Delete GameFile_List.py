#
# 2024.3.31일 
#
# 이프로그램은, 레트로 게임기의 롬파일의 중복된 것을 찾아서,
# 그것을 지워주기 위한 프로그램임
# myfile.txt 에는 토탈커맨더에서, 파일리스트를 가져와서 등록 ...
#
#




import os

# Path to your myfile.txt
myfile_path = "c:\\Users\\minhwasoo\\Downloads\\myfile.txt"
DEL_PATH = "e:\\RetroBat\\roms\\fbneo\\"

def get_filename(file_name):
    # Check if the input string contains a path separator
    if os.path.sep in file_name:
        # Extract and return the filename from the path
        return os.path.basename(file_name)
    else:
        # If no path is found in the string, return the original input
        return file_name


def main():
    try:
        # Open the file in read mode
        with open(myfile_path, 'r') as file:
            # Iterate through each line in the file
            for line in file:
                # Get the filename, stripping any leading/trailing whitespace
                filename = line.strip()
                filename = get_filename(filename)
                
                # Check if the file exists
                if os.path.isfile(DEL_PATH + filename):
                    # Delete the file
                    os.remove(DEL_PATH + filename)
                    print(f"Deleted {filename}")
                else:
                    print(f"{filename} does not exist or has already been deleted.")
    except FileNotFoundError:
        print(f"The file {myfile_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")






if __name__ == "__main__":
    main()




