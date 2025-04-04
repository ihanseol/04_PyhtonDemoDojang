
field="date"
text="this is new world"

field = [f"{field}{{{{{i}}}}}" for i in range(len(text))]
print(len(text), field)

