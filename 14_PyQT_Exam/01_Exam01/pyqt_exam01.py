from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(100,100, 200, 300)
    window.setWindowTitle("My Simple QT App ! ")

    layout = QVBoxLayout()
    label = QLabel("Press the button below ...")
    textbox = QTextEdit()
    button = QPushButton("Press Me")
    button.clicked.connect(lambda: on_clicked(textbox.toPlainText()))

    layout.addWidget(label)
    layout.addWidget(textbox)
    layout.addWidget(button)

    window.setLayout(layout)

    # label = QLabel(window)
    # label.setText("hello world ...")
    # label.setFont(QFont("Arial", 16))
    # label.move(50, 100)


    window.show()
    app.exec_()


def on_clicked(msg):
    # print("hello world ...")
    message = QMessageBox()
    message.setText(msg)
    message.exec_()

if __name__ == '__main__':
    main()



