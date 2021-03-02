# https://youtu.be/BJ-VvGyQxho?list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc
# self - instance variable

class Employee:
    num_of_emps = 0
    raise_amt = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

        Employee.num_of_emps += 1

    def fullname(self):
        return f'{self.first} {self.last}'

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amt)

    @classmethod
    def set_raise_amt(cls, amount):
        cls.raise_amt = amount

    @classmethod
    def from_string(cls, emp_str):
        first, last, pay = emp_str_1.split('-')
        return cls(first, last, pay)

    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or  day.weekday() == 6:
            return False
        return True


emp1 = Employee('corey','hwasoo', 5000)
emp2 = Employee('test','user', 3000)

# Employee.set_raise_amt(1.05)
# print(Employee.raise_amt)
# print(emp1.raise_amt)
# print(emp2.raise_amt)
#

emp_str_1 = 'John-Doe-70000'
emp_str_2 = 'steve-Joe-30000'
emp_str_3 = 'Jane-Duck-50000'


# first, last, pay = emp_str_1.split('-')
# new_emp1 = Employee(first, last, pay)

new_emp1 = Employee.from_string(emp_str_1)

print(new_emp1.email)
print(new_emp1.pay)

print('-'*50)

import datetime
my_date = datetime.date(2016, 7, 11)

print(Employee.is_workday(my_date))








