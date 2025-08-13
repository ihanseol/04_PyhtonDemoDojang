import sys

from PySide6.QtWidgets import QApplication, QDialog
from get_tm_cordinate_ui import Ui_Dialog
import kakao


class MainWindow(QDialog):
    """
    Main application window for fetching TM coordinates for a given address.
    """
    DEFAULT_ADDRESS = "대전시 유성구 장대동 278-13"

    def __init__(self, parent=None):
        """
        Initializes the main window, sets up the UI, and connects signals.
        """
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self._setup_initial_state()
        self._connect_signals()

    def _setup_initial_state(self):
        """Sets the initial text in the UI widgets."""
        self.ui.textEdit.setText(self.DEFAULT_ADDRESS)

    def _connect_signals(self):
        """Connects UI element signals to corresponding slots."""
        self.ui.pushButton.clicked.connect(self.fetch_and_display_coordinates)
        self.ui.pushButton_2.clicked.connect(self.close)

    def fetch_and_display_coordinates(self):
        """
        Fetches TM coordinates for the address in the textEdit using the
        Kakao Maps API and displays the result.
        """
        address = self.ui.textEdit.toPlainText().strip()
        if not address:
            self.ui.plainTextEdit.setPlainText("Please enter an address.")
            return

        try:
            result1, result2, result3 = kakao.get_tm_cordinate(address)

            result_text = f"{result1} {result2} {result3}"
            self.ui.plainTextEdit.setPlainText(result_text)

        except Exception as e:
            error_message = f"An error occurred:\n{e}\n\nPlease check the address or your connection."
            self.ui.plainTextEdit.setPlainText(error_message)
            print(f"Error fetching coordinates for '{address}': {e}")  # Log error for debugging


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('windows')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
