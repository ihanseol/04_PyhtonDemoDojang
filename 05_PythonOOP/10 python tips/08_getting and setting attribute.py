class Person():
    pass

person = Person()


person.first = "min"
person.last = "last"


first_key = 'first'
first_val = 'corey'


# person.first_key = first_val
setattr(person, 'first', 'corey')

setattr(person, first_key, first_val)

first = getattr(person, first_key)
print(first)

print('-'*50)

print(person.first)








