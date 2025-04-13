numbers = [1, 6, 2, 10, 4, 12, 14, 3]

x = next((n for n in numbers if n > 10))
print(x)


x = next((n for n in numbers if n > 50), 0)
print(x)

class Employee:
    def __init__(self, emp_id, name):
        self.emp_id = emp_id
        self.name = name

employees = [Employee(1, 'John'), Employee(2, 'Jane'), Employee(3, 'Dave')]

employee = next((e for e in employees if e.emp_id == 8), None)


if employee:
    print(employee.name)
else:
    print(employee)




