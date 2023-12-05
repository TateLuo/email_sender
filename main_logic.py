import os, configparser, sys
from start_send import Start_send
import schedule
import time
import logging
import traceback
from config_tool import ConfigTool
import sqlite3

class Main:
    def __init__(self):
        self.is_running = True
        self.is_paused = False
        self.is_stopped = False
        self.configTool = ConfigTool()

    def send_email_gap_info(self):
        if not os.path.exists('config.ini'):
            print('配置文件不存在')
            return False
        else:
            config = configparser.ConfigParser()
            config.read('config.ini', encoding = 'utf-8')
            if config.has_option('schedule', 'schedule'):
                schedule_date = config.get('schedule', 'schedule').split(',')
                return schedule_date

    def table_exists(self, db_file, table_name):
        conn = sqlite3.connect(db_file)  # 数据库文件路径
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def work_start(self, worker):
        start_email = Start_send()

        db_name = self.configTool.read_config_database()
        if db_name:
            db_name =db_name[0]
            db_file = os.path.join(self.configTool.dir_path, db_name)
            if os.path.exists(db_file):
                table_name = self.configTool.read_config_database()[1]
                for item in table_name:
                    if self.table_exists(db_file, item):
                        #worker.signal.emit(f'\n开始处理数据库{item}')
                        start_email.start_send(worker, db_file,item)
                    else:
                        worker.signal.emit(f'\n数据表{item}不存在，请检查配置文件')
                        worker.working = True

            else:
                worker.signal.emit(f'\n数据库{db_name}不存在')
                worker.working = True

        else:
            worker.signal.emit(f'\n配置文件不存在或未配置数据库信息')
            worker.working = True