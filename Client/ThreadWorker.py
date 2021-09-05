from PyQt5.QtCore import QThread, pyqtSignal


class ThreadWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(int)
    init = pyqtSignal()


    def run(self):
        while True:
            pass