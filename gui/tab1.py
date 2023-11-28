from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
import sqlite3,os

class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        current_path = os.path.dirname(os.path.abspath(__file__))
        # 获取主目录（也就是当前目录的上一级目录）
        main_directory = os.path.dirname(current_path)
        # 打开选中的文件
        self.db_file = os.path.join(main_directory, 'customer.db')

        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        self.setLayout(hbox)

        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()

        self.listWidget = QListWidget()
        self.tableWidget = QTableWidget()

        self.listWidget.itemClicked.connect(self.showTable)

        vbox1.addWidget(self.listWidget)
        vbox2.addWidget(self.tableWidget)

        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        # 设置列表部件的宽度
        self.listWidget.setMaximumWidth(200)

        # 设置表格部件为只读
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        self.loadTables()

    def loadTables(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            self.listWidget.addItem(table[0])

        conn.close()

    def showTable(self, item):
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
