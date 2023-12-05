import time
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit, QPushButton, QHBoxLayout ,QVBoxLayout, QTextEdit
import sys, time, os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from main_logic import Main 
from config_tool import ConfigTool
from .worker_module import  Worker


class TabHome(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.main = Main()
        self.initUI()
        self.status = "开始"  # 默认状态为开始
        self.init_info_text_edit()

    @pyqtSlot(str)
    def updateTextEdit(self, text):  # Define a slot that updates the QTextEdit
        self.info_text_edit.appendPlainText(text)

    def initUI(self):
        self.info_text_edit = QPlainTextEdit(self)  # Create a QTextEdit instance

        self.start_button = QPushButton('开始')
        self.start_button.clicked.connect(self.buttonClicked)

        '''
        self.pause_button = QPushButton('暂停')
        self.pause_button.clicked.connect(self.pause_work)

        self.resume_button = QPushButton('继续')
        self.resume_button.clicked.connect(self.resume_work)
        '''

        self.stop_button = QPushButton('停止')
        self.stop_button.clicked.connect(self.stop_work)

        layout = QVBoxLayout()
        toolBar = QHBoxLayout()
        toolBar.addWidget(self.start_button)
        #toolBar.addWidget(self.pause_button)
        #toolBar.addWidget(self.resume_button)
        toolBar.addWidget(self.stop_button)
        layout.addWidget(self.info_text_edit)
        layout.addLayout(toolBar)
        self.setLayout(layout)
        
    #初始化文本框中显示的内容   
    def init_info_text_edit(self):
        configTool = ConfigTool() 
        file_path = os.path.join(configTool.dir_path,"readme.html")
        if not self.check_first_time():
            self.info_text_edit.appendPlainText("\r欢迎使用智能邮件系统！\r\r")
        elif os.path.exists(file_path):
            self.info_text_edit.appendHtml(self.read_html_file(file_path))
        else:
            self.info_text_edit.appendPlainText("\r欢迎第一次使用智能邮件系统！\r\r检测到使用手册文件丢失")
    
    # 读取 HTML 文件内容
    def read_html_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            html_text = file.read()
        return html_text    

    
    def check_first_time(self):
        configTool = ConfigTool() 
        file_path = os.path.join(configTool.dir_path,"config.ini")
        if os.path.exists(file_path):
            # 如果文件存在，则说明软件已经被使用过了
            return False
        else:
            # 如果文件不存在，则说明软件是第一次使用
            # 创建一个空的使用信息文件
            with open(file_path, 'w') as f:
                f.write("[stmp_info]\nserver = example\nport = example\nusername = example\npassword = example\n\n[imap_info]\nserver = example\nport = example\nusername = example\npassword = example\n\n[database]\ndb_name = example\ntable_name = example\n\n[schedule]\nschedule = example\n\n[stage_info]\ntime_gap = example\n\n[user_info]\nusername = example\nposition = example\ncompany = example\ncustomize_variable = \{\"0\":\{\"subject\":\"example\",\"username\":\"example\",\"company\":\"example\",\"position\":\"example\"}}\n")
            return True
    

    def buttonClicked(self):
        if self.status == "开始":
            self.start_work()
            if self.worker.working:
                # 执行开始操作
                print("开始")
                self.status = "暂停"
                self.start_button.setText("暂停")
        elif self.status == "暂停":
            self.pause_work()
            # 执行暂停操作
            print("暂停")
            self.status = "继续"
            self.start_button.setText("继续")
        elif self.status == "继续":
            self.resume_work()
            # 执行继续操作
            print("继续")
            self.status = "暂停"
            self.start_button.setText("暂停")


    def start_work(self):
        try:
            self.worker = Worker(self.main.work_start)
            self.worker.signal.connect(self.appendPlainText_text)
            self.worker.start()
            #self.info_text_edit.appendPlainText("\n点击了开始")
        except Exception as e:
            info_text_edit.appendPlainText(str(e))
    
    def pause_work(self):
        if self.worker is not None:
            self.worker.pause()
            #self.info_text_edit.appendPlainText("\n点击了暂止")

    def resume_work(self):
        if self.worker is not None:
            self.worker.resume()
            #self.info_text_edit.appendPlainText("\n点击了继续")

    def stop_work(self):
        self.status = "开始"
        self.start_button.setText("开始")
        if self.worker is not None:
            self.worker.stop()
            self.worker = None
            #self.info_text_edit.appendPlainText("\n点击了停止")

        

    def appendPlainText_text(self, text):
        self.info_text_edit.appendPlainText(text)