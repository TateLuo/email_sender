import time
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QLabel, QFileDialog
import sys, time, os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from .convert import Convert  
from .worker_module import  Worker

class ImportDate(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.convert = Convert()
        self.initUI()
        self.csv_path = ""
    
    @pyqtSlot(str)
    def updateTextEdit(self, text):  # Define a slot that updates the QTextEdit
        self.info_text_edit.append(text)

    def initUI(self):
        self.info_text_edit = QTextEdit(self) 
        self.csv_path_Label = QLabel('', self)    


        choiceButton = QPushButton('选择csv文件', self)
        choiceButton.clicked.connect(self.choiceCSV)    
 
        startButton = QPushButton('开始导入', self)
        startButton.clicked.connect(self.startWork)

        vbox = QVBoxLayout()
        vbox.addWidget(self.csv_path_Label)
        vbox.addWidget(choiceButton)
        vbox.addWidget(startButton)
        vbox.addWidget(self.info_text_edit)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('导入数据')  
        self.show()
        

    def startWork(self):
        if os.path.exists(self.csv_path):
            self.worker = Worker(self.convert.start_convert)
            self.worker.signal.connect(self.append_text)
            self.worker.path = self.csv_path
            self.worker.start()
            self.info_text_edit.append("\n开始导入")
        else:
            self.info_text_edit.append("请先选择正确的csv文件地址！")

    def choiceCSV(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择文件', '/', 'CSV Files (*.csv)')
        if fname:
            #print("文件路径：", fname)
            self.csv_path = fname
            self.info_text_edit.append(f'您已选择文件地址为：{fname}')
    
    def append_text(self, text):
        self.info_text_edit.append(text)
    
    def get_csv_path(self):
        return self.csv_path_Label.text()