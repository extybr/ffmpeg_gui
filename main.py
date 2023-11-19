from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = uic.loadUi("ffmpeg.ui")
    window.show()
    app.setWindowIcon(QIcon('images/favicon.ico'))
    app.exec_()
