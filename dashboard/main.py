from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from gui import MainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())