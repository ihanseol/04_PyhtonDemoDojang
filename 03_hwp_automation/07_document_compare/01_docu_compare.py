import difflib  # 두 개 문자열간의 차이점을 분석하는 데 쓸 수 있는 외장 라이브러리입니다. 설치되어 있어요.

import pyperclip as cb  # 클립보드를 제어할 수 있는 간편한 툴입니다. pip로 설치하세요.
import win32com.client as win32  # 쓰고 계시죠?


def 글자색(Color):  # 먼저 함수를 정의해놓겠습니다.
    """셀 안의 모든 글자색을 바꾼다."""
    hwp.HAction.Run("TableCellBlock")  # F5키를 누르고
    hwp.HAction.Run(f"CharShapeTextColor{Color.capitalize()}")  # 색변경 메서드를 실행 후
    hwp.HAction.Run("Cancel")  # 셀 선택 취소


if __name__ == '__main__':
    hwp = win32.gencache.EnsureDispatch('HWPFrame.HwpObject')  # 한/글 열고
    hwp.RegisterModule("FilePathCheckDLL", "SecurityModule")  # 보안모듈 적용하고,

    hwp.Run("FileNew")  # 새창
    hwp.Open(r"C:\Users\minhwasoo\Desktop\별헤는밤_원본.hwp")  # 원본 열고,
    hwp.Run("FileNew")  # 또 새 창,
    hwp.Open(r"C:\Users\minhwasoo\Desktop\별헤는밤_조작.hwp")  # 조작한 버전 열고,
    hwp.Run("FileNew")  # 또 새 창,
    hwp.Open(r"C:\Users\minhwasoo\Desktop\비교표.hwp")  # 비교표를 작성할 빈 문서입니다.
    # 1행2열의 표가 미리 작성되어 있어요.

    원본 = hwp.XHwpDocuments.Item(1)
    사본 = hwp.XHwpDocuments.Item(2)
    비교 = hwp.XHwpDocuments.Item(3)
    hwp.XHwpDocuments.Add(False)
    추가창 = hwp.XHwpDocuments.Item(4)

    # 문서가 열린 순서대로 인덱스가 매겨집니다.
    # 참고로 방금 실행한 hwp.Run("FileNew") 는 hwp.XHwpDocuments.Add(True)와 같은 명령어입니다.
    # 파라미터로 True 대신 False를 입력하면 새 창이 아니라 새 탭이 열립니다.
    # 새 탭을 사용하면 한/글창 하나만 열고 작업하니까 작업표시줄을 많이 안 잡아먹을 수도 있겠죠?
    # 저는 마우스 클릭이 귀찮아서 그냥 한/글 창을 여러 개 만들어서 작업합니다.

    # 인덱스는 hwp.XHwpDocuments.Item(index)로 접근할 수 있는데,
    # 이 인덱스도 0부터 시작합니다.
    # 2019년 12월 현재 아래아한글 2018 버전 최신 업데이트시
    # 자동화 인스턴스를 생성하면 초기에 백그라운드에서 실행이 됩니다.
    # 이 백그라운드 인스턴스를 나타나게 하는 메서드가 아직 없는 상태여서 무시하고요
    # FileNew 액션으로 새 창을 열고 1번째 인덱스부터 사용을 하는 중입니다.
    # 현재 0번째 인덱스도 열려 있기는 합니다.
    # 이 점 때문에, 한글 자동화작업을 마쳤다고, 닫기버튼을 눌러서 한글을 꺼버리면
    # 백그라운드에서 실행중인 한글창 하나가 열려있는 상태가 돼버립니다.
    # 그래서 자동화를 마치면 무조건 hwp.Quit() 메서드를 실행해서 종료해 주셔야 합니다.
    # 꼭 기억해주세요. 이렇게 종료 안 하시면 백그라운드에 한/글창이 여러 개 띄워져서 메모리와 프로세스를 잡아먹습니다.

    # 하나만 더 말씀을 드리면,
    # 인덱스에 해당하는 한/글 창에 접근하는 방법은 해당 Item() 객체의 SetActive_XHwpDocument() 메서드입니다.
    # 이따가 한 번 더 설명드릴 건데,
    # 꼭 기억해 두셔야 하는 것은 해당 창을 닫고 싶을 때,
    # 아이템 인덱스가 뭐든간에 활성화된 창이 먼저 닫힙니다.
    # 이게 무슨 말이냐면, 원본.Close()를 해도 현재 사본 한글창이 열려 있다면, 원본이 아니라 사본 한글창이 닫힙니다.
    # 처음엔 어리둥절 할 수 있지만, 금방 익숙해지실 거에요.
    # 또 SetActive_XHwpDocument()를 하지 않더라도 마우스로 한글창을 선택하면 활성화상태가 됩니다.
    원본.SetActive_XHwpDocument()  # 원본 활성화
    hwp.InitScan()  # 문서 탐색 초기화 실시(한글에선 탐색시 필수)
    original_full_text = ""  # 빈 문자열을 만들고
    stop_signal = True  # while 문을 사용하기 위해 stop_signal 변수 정의
    while stop_signal:
        signal, text = hwp.GetText()  # GetText 는 튜플을 반환하는데, 일종의 기호와 내용입니다. API 참조
        original_full_text += text  # 탐색한 문자열을 하나씩 더해갑니다.
        if signal == 1:  # 문서 마지막에 도착하면 GetText에서 반환한 튜플값 첫번째 값이 1입니다.
            break  # 그러면 while 문 종료.
    hwp.ReleaseScan()  # InitScan 후에는 꼭 ReleaseScan 을 실행해주셔야 합니다. Open과 Close처럼요.
    original_full_text = original_full_text.split('\r\n')[:-1]  # 문서 마지막의 엔터 때문에 '\r\n'이 리스트의 마지막 원소이므로 마지막 원소는 제거.

    사본.SetActive_XHwpDocument()  # 위와 완전히 동일합니다. 원본과 사본의 문자열만 리스트로 가져옵니다.
    hwp.InitScan()
    copy_full_text = ""
    stop_signal = 1
    while stop_signal:
        signal, text = hwp.GetText()
        copy_full_text += text
        if signal == 1:
            break
    hwp.ReleaseScan()
    copy_full_text = copy_full_text.split('\r\n')[:-1]

    # 이렇게 준비작업을 모두 마쳤습니다.
    # 이제 비교표를 작성하겠습니다.

    비교.SetActive_XHwpDocument()  # 비교표 활성화
    for original_statement in original_full_text:  # 원본 문장을 전부 순회하면서
        cb.copy(original_statement)  # 클립보드에 한 문장씩 복사한 후
        hwp.Run('Paste')  # 표 안에 붙여넣기 하고,
        hwp.Run('TableRightCellAppend')  # 우측 셀로 이동해서
        coupled_dict = dict()
        for copy_statement in copy_full_text:
            coupled_dict[difflib.SequenceMatcher(None, original_statement.split(' ', 1)[1],
                                                 copy_statement.split(' ', 1)[1]).ratio()] = copy_statement
        max_ratio = max(k for k, v in coupled_dict.items())
        cb.copy(coupled_dict[max_ratio].strip())  # 유사도가 제일 높은 문장을 찾아 복사하고,
        hwp.Run('Paste')  # 우측칸에 붙여넣기
        if max_ratio < 1.0:  # 완전히 똑같지 않다면?
            글자색('red')  # 해당 셀의 글자를 빨갛게
        else:
            글자색('black')  # 그렇지 않다면 다시 까맣게. (이건 한/글 버그 때문인데, 위쪽 셀의 글자가 빨간색이면 새로 생성한 아래 셀도 기본적으로 글자색이 빨간색임.)

        hwp.Run('TableRightCellAppend')  # 탭 키를 눌러서 아래에 새 행을 생성. 원본 문장 수만큼 반복!

    hwp.SaveAs(r"c:\users\minhwasoo\desktop\최종본.hwp")
    hwp.Quit()