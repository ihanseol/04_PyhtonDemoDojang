# my_exception.py

class MyException(Exception):
    """
    PHP의 myException 클래스를 대체하는 사용자 정의 예외 클래스입니다.
    """

    def __init__(self, message, code=0):
        super().__init__(message)
        self.code = code

    @staticmethod
    def my_error_handler(errno, errstr, errfile, errline):
        """
        PHP set_error_handler 역할을 하는 정적 메서드 (파이썬에서는 일반적으로 사용되지 않음)
        """
        # 파이썬에서는 기본 예외 처리 방식을 따르는 것이 일반적입니다.
        # 필요하다면 경고를 발생시키거나 로그를 남길 수 있습니다.
        import warnings
        warnings.warn(f"[{errno}] {errstr} in {errfile} line {errline}", UserWarning)
        # False를 반환하면 파이썬의 기본 에러 핸들러가 처리합니다.
        return False
