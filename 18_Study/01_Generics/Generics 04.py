from typing import Callable, Optional


class MyList[T](list):
    def first_or_default(self, pred:Callable[[T], bool]) -> Optional[T]:
        try:
            return next(x for x in self if (pred(x)))
        except StopIteration:
            try:
                generic_type = self.__orig_class__.__args__[0]  #pyright ignore
                return generic_type()
            except TypeError:
                return None



class Employee:
    def __init__(self, emp_id, name):
        self.emp_id = emp_id
        self.name = name


numbers = MyList[int]([4, 8, 12, 6, 11, 21, 2, 3, 4, 5])

print(numbers.first_or_default(lambda x: x > 10))
print(numbers.first_or_default(lambda x: x > 50))

names = MyList[str](["Vera", "Dave", "Ringo", "Leo"])
print(names.first_or_default(lambda x: len(x) > 4))
print(names.first_or_default(lambda x: len(x) > 10))


employee = MyList[Employee]([Employee(1, 'John'), Employee(2, 'Jane'), Employee(3, 'Dave')])
e = employee.first_or_default(lambda x: x.emp_id == 2)

if e:
    print(e.name)
else:
    print(e)

e = employee.first_or_default(lambda x: x.emp_id == 9)

if e:
    print(e.name)
else:
    print(e)




