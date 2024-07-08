import os
import logging

class PathChecker:
    RET_FILE = "retFile"
    RET_DIR = "retDir"
    RET_NOTHING = "retNothing"

    @staticmethod
    def check_path(path):
        if os.path.exists(path):
            if os.path.isfile(path):
                return PathChecker.RET_FILE
            elif os.path.isdir(path):
                return PathChecker.RET_DIR
            else:
                return PathChecker.RET_NOTHING
        else:
            return PathChecker.RET_NOTHING


class FileBase:
    def __init__(self, directory=r'D:\05_Send\\'):
        self._directory = directory
        self._set_directory(directory)

    def _set_directory(self, directory):
        """Set the working directory and refresh the file list."""
        try:
            self._directory = directory
            os.chdir(self._directory)
            self.files = os.listdir(directory)
        except Exception as e:
            print(f"디렉터리를 설정하는 동안 오류가 발생했습니다: {e}")
            self.files = []

    @property
    def directory(self):
        """Getter for the directory."""
        return self._directory

    @directory.setter
    def directory(self, value):
        """Setter for the directory. Refreshes file list if the directory changes."""
        if self._directory != value:
            self._set_directory(value)


class Logger:
    def __init__(self, log_file="app.log"):
        logging.basicConfig(filename=log_file, level=logging.INFO)
        self.logger = logging.getLogger()

    def log(self, message):
        self.logger.info(message)
        print(f"로그: {message}")


class FileManager(PathChecker, FileBase, Logger):
    def __init__(self, directory=r'D:\05_Send\\', log_file="app.log"):
        FileBase.__init__(self, directory)
        Logger.__init__(self, log_file)

    def detailed_file_info(self):
        """Print detailed information about files in the directory."""
        for file in self.files:
            file_path = os.path.join(self._directory, file)
            file_type = self.check_path(file_path)
            info = f"파일 이름: {file}, 유형: {file_type}"
            print(info)
            self.log(info)


def main():
    # FileManager 클래스 테스트
    file_manager = FileManager()
    print(f"현재 디렉터리: {file_manager.directory}")
    print(f"파일 목록: {file_manager.files}")

    # 디렉터리 변경 테스트
    new_directory = input("새 디렉터리를 입력하세요: ")
    file_manager.directory = new_directory
    print(f"변경된 디렉터리: {file_manager.directory}")
    print(f"새 파일 목록: {file_manager.files}")

    # 파일 상세 정보 출력
    file_manager.detailed_file_info()


if __name__ == "__main__":
    main()
