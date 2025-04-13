from typing import List


class IntegerList:
    def __init__(self, elements: List[int]):
        self.elements = elements


class GenericList[T]:
    def __init__(self, elements: List[T]):
        self.elements = elements


i = IntegerList([1, 2, 3])
print(i.elements)

i = GenericList[int]([1, 2, 3])
print(i.elements)

i = GenericList[float]([1.1, 2.3, 3])
print(i.elements)


class IntConverter:
    def convert(self, value: str) -> int:
        if value:
            return int(value)
        else:
            return 0


class FloatConverter:
    def convert(self, value: str) -> float:
        if value:
            return float(value)
        else:
            return 0.0


class GenericConverter[T]:
    def __init__(self):
        self.__orig_class__ = None

    def convert(self, value: str) -> T:
        generic_type = self.__orig_class__.__args__[0]

        if value:
            return generic_type(value)
        else:
            return generic_type()


print(IntConverter().convert("123"))
print(IntConverter().convert(""))

print(FloatConverter().convert("123.1"))
print(FloatConverter().convert(""))

print(GenericConverter[float]().convert("123.1"))
print(GenericConverter[float]().convert(""))


