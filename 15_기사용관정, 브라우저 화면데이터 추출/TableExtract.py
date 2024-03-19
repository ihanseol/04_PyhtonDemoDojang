# pip install beautifulsoup4
# first remove </br> tag
# and find value of data

# print("simdo의 값:", simdo)  - sim do
# print("well_diameter의 값:", well_diameter) - well_diameter
# print("Q의 값:", Q) - Q
# print("HP의 값:", HP) - HP
# print("tochool의 값:", tochool) - tochool


from bs4 import BeautifulSoup

with open(r'c:\Users\minhwasoo\Downloads\info.xls', 'r', encoding='utf-8') as file:
    data = file.read().replace('</br>', '')

print(data)
soup = BeautifulSoup(data, 'html.parser')

simdo = soup.find('th', string='굴착심도(m)').find_next_sibling('td').text

well_diameter = soup.find('th', string='굴착직경(mm)').find_next_sibling('td').text

Q = soup.find('th', string='양수능력(㎥/일)')
if Q is not None:
    Q = Q.find_next_sibling('td').text
else:
    Q = None

HP = soup.find('th', string='동력장치마력(마력)')
if HP is not None:
    HP = HP.find_next_sibling('td').text
else:
    HP = None


tochool = soup.find('th', string='토출관 직경(mm)')
if tochool is not None:
    tochool = tochool.find_next_sibling('td').text
else:
    tochool = None

# 값 출력
print("simdo         :", simdo)
print("well_diameter :", well_diameter)
print("HP            :", HP)
print("Q             :", Q)
print("tochool       :", tochool)


