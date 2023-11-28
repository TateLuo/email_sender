from PyQt5.QtWidgets import QMainWindow, QTabWidget
from config_editor import ConfigEditor
from tab1 import Tab1
from tab2 import Tab2
from tab_home import TabHome

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.tabWidget = QTabWidget(self)
        self.setCentralWidget(self.tabWidget)

        self.tab1 = Tab1()
        self.tab2 = Tab2()
        self.tab_home = TabHome()
        self.tab3 = ConfigEditor()
        
        #self.tabWidget.addTab(self.tab_home, "主页")
        self.tabWidget.addTab(self.tab1, "客户信息")
        self.tabWidget.addTab(self.tab2, "编辑模板")
        self.tabWidget.addTab(self.tab3, "Config Editor")

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Smart Email sender')    
