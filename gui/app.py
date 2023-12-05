from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

class Worker(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.working = True
        self.paused = False

    def run(self):
        for i in range(100):
            if not self.working:
                break

            while self.paused:
                self.msleep(100)

            self.signal.emit(str(i))
            self.msleep(500)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.working = False

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.worker = Worker()
        self.worker.signal.connect(self.append_text)

        self.start_button = QPushButton('开始')
        self.start_button.clicked.connect(self.start_work)

        self.pause_button = QPushButton('暂停')
        self.pause_button.clicked.connect(self.pause_work)

        self.resume_button = QPushButton('继续')
        self.resume_button.clicked.connect(self.resume_work)

        self.stop_button = QPushButton('停止')
        self.stop_button.clicked.connect(self.stop_work)

        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.resume_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

    def start_work(self):
        self.worker.start()

    def pause_work(self):
        self.worker.pause()

    def resume_work(self):
        self.worker.resume()

    def stop_work(self):
        self.worker.stop()

    def append_text(self, text):
        print(text)

app = QApplication([])
window = Window()
window.show()
app.exec_()
