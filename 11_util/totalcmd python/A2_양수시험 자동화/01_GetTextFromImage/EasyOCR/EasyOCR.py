import easyocr

reader = easyocr.Reader(['ko', 'en'])
results = reader.readtext('test.png')
print(results)
