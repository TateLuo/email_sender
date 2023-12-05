from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
import sqlite3,os
from config_tool import ConfigTool


class Tab1(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.init_db_ui()

    def initUI(self):
        hbox = QHBoxLayout()
        self.setLayout(hbox)

        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()

        self.listWidget = QListWidget()
        self.tableWidget = QTableWidget()
        
        try:
            self.listWidget.itemClicked.connect(self.showTable)
        except Exception as e:
            print(str(e))
        vbox1.addWidget(self.listWidget)
        vbox2.addWidget(self.tableWidget)

        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        # 设置列表部件的宽度
        self.listWidget.setMaximumWidth(200)

        # 设置表格部件为只读
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

     
    def init_db_ui(self):
        self.db_file = self.get_all_db_file()
        if self.db_file:
            self.loadTables(self.db_file)
        else:
            self.listWidget.addItem("文件夹中不存在配置文件中的数据库，请导入数据库后重启软件")
    
    def get_all_db_file(self):
        configtool = ConfigTool()
        db_name = configtool.read_config_database()
        if db_name:
            db_name = db_name[0]
            current_path = os.path.dirname(os.path.abspath(__file__))
            # 获取主目录（也就是当前目录的上一级目录）
            main_directory = os.path.dirname(current_path)
            # 扫描目录中所有数据库文件
            db_files = os.path.join(main_directory, db_name)
            if os.path.exists(db_files):
                return db_files
            else:
                return False
        else:
            print('配置文件不存在')
            self.listWidget.addItem("配置文件不存在或未配置数据库信息")

    def loadTables(self,db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            self.listWidget.addItem(table[0])

        conn.close()

    def showTable(self, item):
        if self.db_file:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()

            cursor.execute(f"SELECT * FROM {item.text()}")
            rows = cursor.fetchall()

            self.tableWidget.setRowCount(len(rows))
            self.tableWidget.setColumnCount(len(rows[0]))

            # 获取并设置表头
            headers = [description[0] for description in cursor.description]
            self.tableWidget.setHorizontalHeaderLabels(headers)

            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))
            conn.close()
