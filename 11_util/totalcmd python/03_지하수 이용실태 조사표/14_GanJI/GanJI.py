def get_sixty_ganji(year):
    zodiac = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
    animal = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

    # 연도를 4로 나눈 나머지로 띠를 결정
    index = year % 12
    animal_sign = animal[index]

    # 연도를 12로 나눈 나머지로 천간을 결정
    index = (year - (year % 12)) // 12
    zodiac_sign = zodiac[index]

    return f"{zodiac_sign}{animal_sign}"

year = int(input("년도를 입력하세요: "))
ganji = get_sixty_ganji(year)
print(f"{year}년은 {ganji}년 입니다.")