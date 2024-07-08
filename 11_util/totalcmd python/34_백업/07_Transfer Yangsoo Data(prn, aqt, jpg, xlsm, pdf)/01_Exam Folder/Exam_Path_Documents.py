import os

documents = os.path.expanduser("~\\Documents")

print(documents)

joinpath = os.path.join(documents, "a1_save.dat")
joinpath = joinpath.replace("/","\\")
print(joinpath)

