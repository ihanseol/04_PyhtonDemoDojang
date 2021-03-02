# https://youtu.be/ZDa-Z5JzLYM?list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc

class Employee:
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'

    def fullname(self):
        return f'{self.first} {self.last}'



emp1 = Employee('corey','hwasoo', 5000)
emp2 = Employee('test','user', 3000)


print(emp1.email)
print(emp2.email)

print(emp1.fullname())
print(Employee.fullname(emp1))





