# https://youtu.be/K36DX1hYoow
from itertools import starmap
from typing import Callable, Iterator


def int_to_x(n: int) -> str:
    return n * 'X'


def IterExam():
    int_to_x2: Callable[[int], str] = lambda n: n * 'x'
    mapped_01: Iterator[str] = map(int_to_x, [1, 2, 3, 4])
    mapped_02: Iterator[str] = map(lambda n: n * 'x', [1, 2, 3, 4])

    print(int_to_x(10))
    print(int_to_x2(10))
    print(list(mapped_01))
    print(list(mapped_02))


def multiply_str(text: str, n: int) -> str:
    return text * n


multiply_str2: Callable[[str, int], str] = lambda text, n: text * n

data: list[tuple[str, int]] = [('bob', 3), ('X', 6), ('A', 3)]
# sm : starmap

sm: Iterator[str] = starmap(multiply_str2, data)
sm2: Iterator[str] = starmap(lambda s, n: s * n, data)


def Exam_03():
    res = (lambda s : print(f'{(s*3).capitalize()}'))('yo')
    print(res)

def Exam_04():
    display_list: Callable[[str], None] = lambda s: print(*s, sep=', ', end='\n')
    display_list(['Bob', 'James', 'Cowork'])
    display_list([1, 2, 3])


if __name__ == '__main__':
    # IterExam()
    print(multiply_str2('a', 5))
    print(data)
    print(list(sm2))
    Exam_04()

