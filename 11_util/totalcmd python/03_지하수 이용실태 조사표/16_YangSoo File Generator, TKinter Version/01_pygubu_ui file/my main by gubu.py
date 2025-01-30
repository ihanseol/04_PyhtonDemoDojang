import tkinter as tk
import tkinter.ttk as ttk
import pygubu


class MainWindow:
    def __init__(self, master=None):
        self.builder = pygubu.Builder()
        self.builder.add_from_file('pygubu.ui')
        self.mainwindow = self.builder.get_object('mainframe', master)

        # Connect callbacks here
        self.builder.connect_callbacks(self)


if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
