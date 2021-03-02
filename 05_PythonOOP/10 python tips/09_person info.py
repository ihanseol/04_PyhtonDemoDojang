class Person():
    pass

person = Person()

person_info = {'first':'Corey', 'last': 'schafer'}

for key, value in person_info.items():
    setattr(person, key, value)

print(person.first)
print(person.last)


for key in person_info.keys():
    print(getattr(person, key))


