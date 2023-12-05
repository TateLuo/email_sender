from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    update_text = pyqtSignal(str)  # Add a signal
    signal = pyqtSignal(str)
    path = None



    def __init__(self, loop_function):
        super().__init__()
        self.working = True
        self.paused = False
        self.loop_function = loop_function

    def run(self):
        self.loop_function(self)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.working = False
