from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow

from LoadingScreen import run

if __name__ == "__main__":
    run()
class X(QMainWindow):
    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(a0)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(a0)

