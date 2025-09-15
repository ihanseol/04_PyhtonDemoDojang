import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QListWidget, QTextEdit, QAbstractItemView, QSizePolicy
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class BleachBitLikeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BleachBit-like GUI")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # 왼쪽 목록 창 (ListWidget)
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_widget.setFixedWidth(200)

        # 항목 추가
        self.list_widget.addItem("System")
        self.list_widget.addItem("Clipboard")
        self.list_widget.addItem("Custom")
        self.list_widget.addItem("Free disk space")
        self.list_widget.addItem("Logs")
        self.list_widget.addItem("Memory dump")
        self.list_widget.addItem("MuiCache")
        self.list_widget.addItem("Prefetch")
        self.list_widget.addItem("Recycle bin")
        self.list_widget.addItem("Temporary files")

        main_layout.addWidget(self.list_widget)

        # 오른쪽 텍스트 출력 창 (TextEdit)
        self.text_editor = QTextEdit()
        self.text_editor.setReadOnly(True)  # 읽기 전용으로 설정
        self.text_editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_editor.setFont(QFont("Consolas", 10)) # 가독성을 위해 폰트 설정

        main_layout.addWidget(self.text_editor)

        self.setLayout(main_layout)

        # gui_print 함수 연결
        self.gui_print("GUI 초기화 완료.\n")
        self.gui_print("데이터를 출력합니다...\n")

    def gui_print(self, *args, sep=' ', end='\n'):
        """
        텍스트 에디터에 내용을 출력하는 함수.
        일반 print() 함수처럼 동작합니다.
        """
        message = sep.join(map(str, args)) + end
        self.text_editor.insertPlainText(message)
        self.text_editor.verticalScrollBar().setValue(self.text_editor.verticalScrollBar().maximum()) # 스크롤을 항상 최하단으로

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = BleachBitLikeApp()
    ex.show()

    # gui_print 함수 사용 예시
    for i in range(20):
        ex.gui_print("--- 로그 출력 시작 ---")
        ex.gui_print("Delete 0B C:\\Windows\\SoftwareDistribution\\Download\\...")
        ex.gui_print("Delete 0B C:\\Windows\\SoftwareDistribution\\Download\\...")
        ex.gui_print("Delete 0B C:\\Windows\\SoftwareDistribution\\Download\\...")
        ex.gui_print("Disk space recovered:", "835MB")
        ex.gui_print("Files deleted:", 72131)
        ex.gui_print("Special operations:", 2)
        ex.gui_print("Traceback (most recent call last):")
        ex.gui_print("--- 로그 출력 종료 ---")

    sys.exit(app.exec())