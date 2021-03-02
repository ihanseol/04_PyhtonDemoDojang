
class Employee:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def email(self):
        return self.first + '.' + self.last + '@company.com'

    @property
    def fullname(self):
        return f'{self.first} {self.last}'

    @fullname.setter
    def fullname(self, name):
        first, last = name.split(' ')
        self.first = first
        self.last = last

    @fullname.deleter
    def fullname(self):
        print('Delete Name!')
        self.first =  None
        self.last = None


emp1 = Employee('corey','hwasoo')
emp2 = Employee('test','user')

print(emp1.fullname)
print(emp1.email)

emp1.fullname = 'min hwasoo'

print(emp1.fullname)

del emp1.fullname

print(emp1.fullname)







