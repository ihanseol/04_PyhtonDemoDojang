# https://youtu.be/RSl87lqOXDE?list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc
# self - inheritance and make sub class

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

class Developer(Employee):
    raise_amt = 1.10

    def __init__(self, first, last, pay, prog_lang):
        super().__init__(first, last, pay)
        self.prog_lang = prog_lang
        # Employee.__init__(self, first, last, pay)


class Manager(Employee):
    def __init__(self, first, last, pay, employees=None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)

    def print_emps(self):
        for emp in self.employees:
            print('-->', emp.fullname())


emp1 = Employee('corey','hwasoo', 5000)
emp2 = Employee('test','user', 3000)

dev1 = Developer('corey','hwasoo', 5000, 'Python')
dev2 = Developer('test','user', 3000, 'Java')


print(dev1.email)
print(dev1.prog_lang)

# print(help(Developer))

print(dev1.pay)
dev1.apply_raise()
print(dev1.pay)


mgr1 = Manager('Sue', 'Smith', 9000, [dev1])
print(mgr1.email)
mgr1.print_emps()

print('-'*50)

mgr1.add_emp(dev2)
mgr1.print_emps()

print('-'*50)

print(isinstance(mgr1, Developer))

print(issubclass(Manager, Employee))
print(issubclass(Manager, Developer))
print(issubclass(Employee, Manager))



















