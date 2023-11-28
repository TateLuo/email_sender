import os
import sqlite3
import json
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QTableWidget, QPushButton
from datetime import datetime

class TabHome(QWidget):
    def __init__(self, parent=None):
        super(TabHome, self).__init__(parent)
        self.setWindowTitle("客户邮件管理")

       # 创建网格布局
        layout = QGridLayout()

        # 创建四个区域，每个区域对应一个功能
        self.customer_overview = QLabel()
        self.email_overview = QLabel()
        self.sender_overview = QLabel()
        self.function_area = QPushButton("开始发送邮件")

        # 将这些控件添加到布局中
        layout.addWidget(QLabel("客户信息总览"), 0, 0)
        layout.addWidget(self.customer_overview, 1, 0)
        layout.addWidget(QLabel("邮件信息总览"), 0, 1)
        layout.addWidget(self.email_overview, 1, 1)
        layout.addWidget(QLabel("发件信息总览"), 2, 0)
        layout.addWidget(self.sender_overview, 3, 0)
        layout.addWidget(QLabel("功能区"), 2, 1)
        layout.addWidget(self.function_area, 3, 1)

        # 设置窗口的布局
        self.setLayout(layout)

        # 连接到数据库并获取数据
        self.data = self.get_data_from_db()

        # 根据获取的数据更新界面
        self.update_ui()

    def get_data_from_db(self):
        # 获取数据库的路径
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'your_database_name.db')

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 获取所有表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        data = {}
        for table in tables:
            if table[0] == 'sqlite_sequence':
                continue
            cursor.execute(f'SELECT * FROM {table[0]}')
            data[table[0]] = cursor.fetchall()

        conn.close()
        return data

    def update_ui(self):
        # 在这里根据获取的数据更新界面
        total_send_times = 0
        country_send_times = {}
        for country, rows in self.data.items():
            send_times = sum(json.loads(row[2])['send']['send_times'] for row in rows)
            total_send_times += send_times
            country_send_times[country] = send_times

        self.email_overview.setText(f'总共发送了 {total_send_times} 次邮件\n' + '\n'.join(f'{country}: {times}' for country, times in country_send_times.items()))

        latest_send_time = max((json.loads(row[2])['send']['last_send_date'] for country, rows in self.data.items() for row in rows if 'last_send_date' in json.loads(row[2])['send']), default=None)
        due_emails_count = sum(1 for country, rows in self.data.items() for row in rows if json.loads(row[2])['send']['next_send_date'] < datetime.now().isoformat())
        total_receive_times = sum(json.loads(row[2])['receive']['receive_times'] for country, rows in self.data.items() for row in rows)
        country_receive_times = {country: sum(json.loads(row[2])['receive']['receive_times'] for row in rows) for country, rows in self.data.items()}

        self.sender_overview.setText(f'最近邮件发送时间：{latest_send_time}\n已到发送时间的邮件数量：{due_emails_count}\n总共收到邮件数量：{total_receive_times}\n' + '\n'.join(f'{country}: {times}' for country, times in country_receive_times.items()))
