# unpacking
a, b = (1,2)
print(a)
print(b)
print('-'*50)

a,b,*c = (1,2,3,4,5)
print(a)
print(b)
print(c)

print('-'*50)
a, b, *_ = (1,2,3,4,5)
print(a)
print(b)

print('-'*50)
a, b, *c, d = (1,2,3,4,5)
print(a)
print(b)
print(c)
print(d)





