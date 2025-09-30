# 텍스트로만 구성된 10,000 페이지 분량의 문서가 있다.
# 그런데 내용이 없는(비어있는) 페이지가 절반이나 된다.
# 비어있는 페이지만 제거후 PDF로 저장하고 싶다면

# 1, 커서가 있는 현재 페이지에 내용이 있는지 여부?
# 2, 페이지를 통째로 삭제하는 기능이 있는지 여부
# 3, 한페이지를 삭제하는 기능
# 4, PDF로 저장하는 기능,

# hwp = Hwp(new=False)
# 새로운 창을 띠우는 것은, 관리자 권한으로 실행해서 차이가 생겼다.
# 그냥 일반 유저모드로 실행하면 문제가 없다.


# 줄바꿈과, 빈칸은 빈문서로 간주한다.

# 소문자로만 (스네이크 케이스) --
# 캐멀케이스 - API 의 메서드를 그대로 사용하는 경우나,
# 캐멀케이스 - Run 액션명 일 경우에

from pyhwpx import Hwp

hwp = Hwp(new=False)
hwp.get_page_text(4).replace("\r\n", "").replace(" ", "")


# 페이지를 순회하는 방법
#
# hwp를 한번더 부치면 직접 API 를 호출할수가 있다.
# hwp.hwp.XHwpDocuments.Item(0).XHwpDocumentInfo.CurrentPage
# 이것은 0
# hwp.current_page
# 아래아 한글에서 관리하는 페이지 처음은 1
# 두개가 차이가 난다.
# hwp.current_printpage , 1부터 시작, 이것은 쪽번호를 부치면 그 쪽번호를 따라간다.
# pyhwp 에서는 1부터 시작하게 만들었음
#
# hwp.get_page_text() 첫페이지가 0 부터 시작한다.
# hwp.hwp.XHwpDocuments.Item(0).XHwpDocumentInfo.CurrentPage 이것과 동일한 메소드



def is_empty_page(pgno: int = 0):
    if pgno > 0:
        hwp.goto_page(pgno)
    else:
        pgno = hwp.current_page

    content = hwp.get_page_text(pgno).replace("\r\n", "").replace(" ", "")
    if not content:
        return True
    else:
        return False



is_empty_page()

hwp.MoveDocBegin()
for i in range(1, hwp.PageCount+1):
    if is_empty_page(i):
        print(i, "is Empty page ...")


# 순서대로 페이지를 지우면, 페이지 번호들이 모두 리셋되어 당겨온다.
# 그래서 페이지를 지우려면, 거꾸로 지우면 된다.

for i in range(hwp.PageCount, 0, -1):
    if is_empty_page(i):
        print(i, "is Empty page ...")
        hwp.goto_page(i)
        hwp.DeletePage()


"""
# - "HWP": 한/글 native format
# - "HWP30": 한/글 3.X/96/97
# - "HTML": 인터넷 문서
# - "TEXT": 아스키 텍스트 문서
# - "UNICODE": 유니코드 텍스트 문서
# - "HWP20": 한글 2.0
# - "HWP21": 한글 2.1/2.5
# - "HWP15": 한글 1.X
# - "HWPML1X": HWPML 1.X 문서 (Open만 가능)
# - "HWPML2X": HWPML 2.X 문서 (Open / SaveAs 가능)
# - "RTF": 서식 있는 텍스트 문서
# - "DBF": DBASE II/III 문서
# - "HUNMIN": 훈민정음 3.0/2000
# - "MSWORD": 마이크로소프트 워드 문서
# - "DOCRTF": MS 워드 문서 (doc)
# - "OOXML": MS 워드 문서 (docx)
# - "HANA": 하나워드 문서
# - "ARIRANG": 아리랑 문서
# - "ICHITARO": 一太郞 문서 (일본 워드프로세서)
# - "WPS": WPS 문서
# - "DOCIMG": 인터넷 프레젠테이션 문서(SaveAs만 가능)
# - "SWF": Macromedia Flash 문서(SaveAs만 가능)
"""

hwp.save_as("빈페이지제거.dpf", format="PDF")


# 페이지에 그림이나 테이블이 있어도 비어있는 페이지로 나온다.
hwp.is_empty_page()









