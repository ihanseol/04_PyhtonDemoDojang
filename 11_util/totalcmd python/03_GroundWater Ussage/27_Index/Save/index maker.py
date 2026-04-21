# 2026/04/21
# 목적 : 목차를 찾아서, 목차파일을 생성해주는데 목적이 있다.
# 그동안 목차를 저일하는데, 그냥 하나하나 검색하고 적어주고
# 이것을 무한반복했는데
# 이것을 코드로 바꾸어 주려한다.
#
#


from pyhwpx import Hwp


def get_pages_with_text_scan(hwp, search_text):
    """
    init_scan과 get_text를 사용하여 텍스트를 검색하고 페이지 번호를 리스트로 반환함.
    """
    pages = set()

    # 1. 스캔 초기화 (기본값: 문서 전체 대상)
    if not hwp.init_scan():
        return []

    try:
        while True:
            # 2. 텍스트 추출
            state, text = hwp.get_text()

            # state가 0 또는 1이면 문서 끝에 도달한 것이므로 종료
            if state <= 1:
                break

            # 3. 추출된 텍스트에 검색어가 포함되어 있는지 확인
            if search_text in text:
                # 해당 문단으로 캐럿(커서) 이동
                hwp.move_pos(201)

                # 현재 커서 위치의 페이지 번호 추출 (인덱스 1이 페이지)
                page_no = hwp.KeyIndicator()[1]
                pages.add(page_no)

        return sorted(list(pages))

    finally:
        # 4. 스캔 정보 초기화 (반드시 호출해야 함)
        hwp.release_scan()


# 실행 예시
if __name__ == "__main__":
    # 사용 예시
    file_name = r"d:\06_Send3\A1_세종시 연서면 신대리 571 - 2026 영향조사서.hwp"
    hwp = Hwp(visible=False)
    # hwp = Hwp()

    hwp.open(file_name)
    target_text = "영향조사 결과의 요약"
    pages = get_pages_with_text_scan(hwp, target_text)
    print(f"검색어 '{target_text}'가 발견된 페이지: {pages}")
    current_page = hwp.KeyIndicator()[3]
    print(f"현재 페이지: {current_page}")


    target_text = "지하수 이용방안"
    pages = get_pages_with_text_scan(hwp, target_text)
    print(f"검색어 '{target_text}'가 발견된 페이지: {pages}")
    current_page = hwp.KeyIndicator()[3]
    print(f"현재 페이지: {current_page}")

    target_text = "조사서 작성에 관한 사항"
    pages = get_pages_with_text_scan(hwp, target_text)
    print(f"검색어 '{target_text}'가 발견된 페이지: {pages}")
    current_page = hwp.KeyIndicator()[3]
    print(f"현재 페이지: {current_page}")



    target_text = "II. 수문지질현황 및 원수의 개발가능량"
    pages = get_pages_with_text_scan(hwp, target_text)

    print(f"검색어 '{target_text}'가 발견된 페이지: {pages}")
    current_page = hwp.KeyIndicator()[3]
    print(f"현재 페이지: {current_page}")

    # ----------------------------------------------------------------------------

    target_text = "2. 조사지역의 지하수 함양량, 개발가능량 조사"
    pages = get_pages_with_text_scan(hwp, target_text)

    print(f"검색어 '{target_text}'가 발견된 페이지: {pages}")
    current_page = hwp.KeyIndicator()[3]
    print(f"현재 페이지: {current_page}")

    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------

    target_text = "3. 신규 지하수 개발가능량 산정"
    pages = get_pages_with_text_scan(hwp, target_text)

    print(f"검색어 '{target_text}'가 발견된 페이지: {pages}")
    current_page = hwp.KeyIndicator()[3]
    print(f"현재 페이지: {current_page}")

    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------

    target_text = "III. 적정취수량 및 영향범위 산정"
    pages = get_pages_with_text_scan(hwp, target_text)

    print(f"검색어 '{target_text}'가 발견된 페이지: {pages}")
    current_page = hwp.KeyIndicator()[3]
    print(f"현재 페이지: {current_page}")

    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------

    target_text = "2. 적정취수량과 영향반경"
    pages = get_pages_with_text_scan(hwp, target_text)

    print(f"검색어 '{target_text}'가 발견된 페이지: {pages}")
    current_page = hwp.KeyIndicator()[3]
    print(f"현재 페이지: {current_page}")

    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------

    target_text = "3. 잠재오염원과 영향범위"
    pages = get_pages_with_text_scan(hwp, target_text)

    print(f"검색어 '{target_text}'가 발견된 페이지: {pages}")
    current_page = hwp.KeyIndicator()[3]
    print(f"현재 페이지: {current_page}")

    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------

    target_text = "IV. 수질의 적정성 평가"
    pages = get_pages_with_text_scan(hwp, target_text)

    print(f"검색어 '{target_text}'가 발견된 페이지: {pages}")
    current_page = hwp.KeyIndicator()[3]
    print(f"현재 페이지: {current_page}")

    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------

    target_text = "Ⅴ. 시설설치계획"
    pages = get_pages_with_text_scan(hwp, target_text)

    print(f"검색어 '{target_text}'가 발견된 페이지: {pages}")
    current_page = hwp.KeyIndicator()[3]
    print(f"현재 페이지: {current_page}")

    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------

    target_text = "2. 사후 관리방안"
    pages = get_pages_with_text_scan(hwp, target_text)

    print(f"검색어 '{target_text}'가 발견된 페이지: {pages}")
    current_page = hwp.KeyIndicator()[3]
    print(f"현재 페이지: {current_page}")

    # ----------------------------------------------------------------------------

    # ----------------------------------------------------------------------------

    target_text = "<  참 고 문 헌  >"
    pages = get_pages_with_text_scan(hwp, target_text)

    print(f"검색어 '{target_text}'가 발견된 페이지: {pages}")
    current_page = hwp.KeyIndicator()[3]
    print(f"현재 페이지: {current_page}")

    # ----------------------------------------------------------------------------
