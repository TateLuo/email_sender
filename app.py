import sys
import time
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit
from start_send import Start_send  # Assuming start_send is the module and Start_send is the class

class WorkerThread(threading.Thread):
    def __init__(self, schedule_times, db_name, table_names):
        super().__init__()
        self.schedule_times = schedule_times
        self.db_name = db_name
        self.table_names = table_names
        self.running = True
        self.paused = False
        self.Start_send = Start_send()

    def run(self):
        while self.running:
            if not self.paused:
                current_time = time.strftime('%H:%M', time.localtime())
                if current_time in self.schedule_times:
                    for table_name in self.table_names:
                        QApplication.instance().info_text_edit.append(f'开始处理数据库{table_name}')  # Update the text of the QTextEdit
                        self.Start_send.start_send(self.db_name, table_name)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.running = False

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.schedule_times = ['14:32','15:53','16:33','20:38','22:49']  # Replace this with the result of send_email_gap_info(self)
        self.db_name = "your_db_name"  # Replace this with your database name
        self.table_names = ["table1", "table2"]  # Replace this with your table names
        self.worker = WorkerThread(self.schedule_times, self.db_name, self.table_names)
        self.info_text_edit = QTextEdit(self)  # Create a QTextEdit instance
        self.initUI()

    def initUI(self):
        startButton = QPushButton('Start', self)
        startButton.clicked.connect(self.startWork)

        pauseButton = QPushButton('Pause', self)
        pauseButton.clicked.connect(self.pauseWork)

        stopButton = QPushButton('Stop', self)
        stopButton.clicked.connect(self.stopWork)

        vbox = QVBoxLayout()
        vbox.addWidget(startButton)
        vbox.addWidget(pauseButton)
        vbox.addWidget(stopButton)
        vbox.addWidget(self.info_text_edit)  # Add the QTextEdit to the layout

        self.setLayout(vbox)
        self.setWindowTitle('PyQt5 with threading')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def startWork(self):
        if not self.worker.is_alive():
            self.worker = WorkerThread(self.schedule_times, self.db_name, self.table_names)
            self.worker.start()

    def pauseWork(self):
        self.worker.pause()

    def stopWork(self):
        self.worker.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
