# https://youtu.be/BJ-VvGyQxho?list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc

class Employee:
    num_of_emps = 0
    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

        Employee.num_of_emps += 1

    def fullname(self):
        return f'{self.first} {self.last}'

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)



print("Employee.num_of_emps  : " + str(Employee.num_of_emps))

emp1 = Employee('corey','hwasoo', 5000)
emp2 = Employee('test','user', 3000)


print(emp1.pay)
emp1.apply_raise()
print(emp1.pay)

print(Employee.__dict__)
emp1.raise_amount = 1.05
print(emp1.__dict__)


print(Employee.raise_amount)
print(emp1.raise_amount)
print(emp2.raise_amount)

print("Employee.num_of_emps  : " + str(Employee.num_of_emps))











