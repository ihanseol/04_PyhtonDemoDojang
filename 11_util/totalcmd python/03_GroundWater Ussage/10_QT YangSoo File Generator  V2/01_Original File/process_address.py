def process_address(input_str):
    """
    :param input_str:
        주어진 주소값을 입력받고, 그 주소가 길면
        그 주소를 정해진 규칙에 의해서 잘라서
        반환한다.
        aqtsolv project_info 의 주소길이에 맟추어서

        부여읍,신정리177,실지번,산37-1 <-- AqtSolver 에 들어가는 최대치
        글자의 갯수로 20자이다.

    :return:
    """

    input_str = input_str.replace('특별', '').replace('광역', '')
    if ',' in input_str:
        input_str = input_str.split(',')[0]

    if '(' in input_str:
        input_str = input_str.split('(')[0]


    if len(input_str) >= 18:
        if input_str.endswith('호'):
            input_str = input_str.replace('번지 ', '-')
            input_str = input_str[0:-1]
        else:
            input_str = input_str.replace('번지', '')

        parts = input_str.split(' ')
        i = 0

        for part in parts:
            if part.endswith('도') or part.endswith('시') or part.endswith('구') or part.endswith('동'):
                break
            i += 1

        result = ' '.join(parts[(i + 1):])
        address_list = result.split(' ')

        filtered_list = [item for item in address_list if not (item.endswith('아파트') or item == ',')]
        address_string = ' '.join(filtered_list)

        return address_string
    else:
        return input_str


def main():
    # a = '경기도 안양시 동안구 호계동 1001번지 28호'
    # a = '세종특별자치시 부강면 금호리 501번지 1호'

    # a = '대전광역시 서구 영골길 158, (서구 오동 276번지)'
    # a = '충청남도 계룡시 엄사면 유동리 236-2'

    # a = '충청남도 당진시 송악읍 신평로 1469 (동부제강(주)사원임대아파트)'
    # a = '충청남도 당진시 순성면 순성로 453-30 '
    # a = '충청남도 당진시 송악읍 반촌리 374-3 번지 , 동진아파트'
    a = ' 충청남도 보령시 남포면 양기리 285-1 (보령시 남포면 월전로 697-20)'
    a = process_address(a)
    print(a, len(a))


if __name__ == '__main__':
    main()
