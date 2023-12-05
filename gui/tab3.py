import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from .config_editor import ConfigEditor
from .import_data import ImportDate

class Tab3(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.btn_config = QPushButton('编辑配置文件', self)
        self.btn_config.clicked.connect(self.openConfigWindow)
        
        self.btn_import = QPushButton('导入数据', self)
        self.btn_import.clicked.connect(self.importdata)

        vbox = QVBoxLayout()
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_config)
        btn_layout.addWidget(self.btn_import)
        vbox.addLayout(btn_layout)
        
        self.setLayout(vbox)
        self.show

    def openConfigWindow(self):
        self.configWin = ConfigEditor()
        self.configWin.show()
    
    def importdata(self):
        self.import_data = ImportDate()
        self.import_data.show()
