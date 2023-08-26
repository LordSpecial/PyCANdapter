from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader

import sys

from MainWindow import MainWindow


def main():

    # sys.argv += ['--style', 'Fusion']

    app = QApplication()  # (sys.argv)

    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
