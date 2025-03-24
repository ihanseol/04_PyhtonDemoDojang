# https://youtu.be/Ob8PUkdMlxE


from itertools import chain
from typing import Iterator
from sys import getsizeof
from string import ascii_letters


def exam01():
    my_lists: list[list[int]] = [[1, 2, 3], [111, 222]]
    my_chain: Iterator[int] = chain.from_iterable(my_lists)
    print(list(my_chain))


def exam02():
    print(ascii_letters)
    iter1: Iterator[str] = iter(ascii_letters)
    iter2: Iterator[int] = iter(range(1_000_000))
    my_chain: Iterator[str | int] = chain(iter1, iter2)

    print(getsizeof(iter1), 'byters')
    print(getsizeof(iter2), 'bytes')
    print(getsizeof(my_chain), 'bytes')

    extracted: list[str | int] = list(my_chain)
    print(extracted)



if __name__ == '__main__':
    exam02()
