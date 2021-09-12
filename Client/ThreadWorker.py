from PyQt5.QtCore import QThread, pyqtSignal


class ThreadWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(int)

    def run(self):
        while True:
            pass
