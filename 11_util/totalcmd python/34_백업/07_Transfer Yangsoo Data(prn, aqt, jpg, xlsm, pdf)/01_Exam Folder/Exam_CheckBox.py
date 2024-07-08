import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.checkbox = QCheckBox('Check me', self)

        self.toggle_button = QPushButton('Toggle CheckBox', self)
        self.toggle_button.clicked.connect(self.toggle_checkbox)

        layout = QVBoxLayout()
        layout.addWidget(self.checkbox)
        layout.addWidget(self.toggle_button)

        self.setLayout(layout)
        self.setWindowTitle('QCheckBox Example')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def toggle_checkbox(self):
        current_state = self.checkbox.isChecked()
        self.checkbox.setChecked(not current_state)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
