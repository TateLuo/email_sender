import sqlite3
import os
from email_managment import Email_managment
import json
import configparser
import logging
from check_stage import get_email_template, get_send_time_gap
import datetime
import time
from config_tool import ConfigTool


class Start_send:
    def __init__(self):
        self.init_log() #初始化日志工具
        self.init_email_info() #初始化发件邮箱配置
        self.init_other()
        self.configTool = ConfigTool()

    #初始化一些其他的变量
    def init_other(self):
        #时间格式
        self.time_format = "%Y-%m-%d %H:%M:%S"

    #配置日志
    def init_log(self):
        # 获取当前程序所在目录
        self.dir_path = os.getcwd()
        # 配置日志输出到文件
        logging.basicConfig(filename=os.path.join(self.dir_path, 'logfile.log'), level=logging.DEBUG)
        # 在代码中使用日志
        '''
        logging.debug('这是一个debug级别的日志')
        logging.info('这是一个info级别的日志')
        logging.warning('这是一个warning级别的日志')
        logging.error('这是一个error级别的日志')
        logging.critical('这是一个critical级别的日志')
        '''
    
    #初始化发件邮箱配置
    def init_email_info(self):
        configTool = ConfigTool()
        email_server_info = configTool.read_email_info_config()
        #print(email_server_info)
        if email_server_info:
        # 设置SMTP服务器信息
            self.server = email_server_info[0]
            self.port = email_server_info[1]
            self.username = email_server_info[2]
            self.password = email_server_info[3]    
    
    #检查数据库是否存在，不存在则创建    
    def check_database(self, db_file):
        if not os.path.exists(db_file):
            open(db_file, 'w').close()
    
    #从数据库获取
    def get_data(self,db_file, table_name):
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_file)

        # 创建游标对象
        cur = conn.cursor()

        # 构建查询字符串，使用占位符来代表表名
        query = "SELECT * FROM {}".format(table_name)

        # 执行SELECT查询
        cur.execute(query)

        # 获取所有结果
        results = cur.fetchall()
        
        # 关闭游标和连接
        cur.close()
        conn.close()
        print(results)
        return results
    
    #开始发送
    def start_send(self, worker, db_file, table_name):
        #读取数据库输入，参数（库名，表名）
        data = self.get_data(db_file, table_name)
        #print(data)
        #遍历数据
        #row[0] id
        #row[1] company
        #row[2] email_info
        #row[3] contacts
        #row[4] email_status
        pause_printed = False
        for row in data:
            if not worker.working:
                worker.signal.emit(f'\r已停止发送{table_name}')
                break
            while worker.paused:
                if not pause_printed:
                    worker.signal.emit(f'\r\t暂停中')
                    pause_printed = True
                worker.msleep(100)
            
            pause_printed = False  # Reset the flag for the next row
            #先把从数据库中的数据解析出来
            id = row[0]
            company = row[1]
            email_info = row[2]
            print(f'\n开始处理数据，序号：{id}，公司：{company}')
            worker.signal.emit(f'\n开始处理数据库{table_name}，序号：{id}，公司：{company}')
            #判断email_status(row[3])是否为空，为空则初始化一下
            print(row)
            if not row[4]:    
                #联系人和右键状态是json数据，需要json解析
                self.modfiy_email_status(                            
                    db_file,
                    id,
                    table_name,
                    send_times = "0",
                    last_send_date = "2021-11-13 23:44:03",
                    next_send_date = "2021-11-13 23:44:03",
                    error_times = 0,
                    switch = "on",
                    receive_times = 0,
                    last_receive_date = 0)
                #一个多行字符串,初始的email_status数据
                data = """{
                    "send": 
                        {
                            "send_times": "0",
                            "last_send_date": "2021-11-13 23:44:03",
                            "next_send_date": "2021-11-13 23:44:03",
                            "error_times": 0,
                            "switch":"on"},
                    "receive": 
                        {
                            "receive_times": 0, 
                            "last_receive_date": 0}
                        }"""
                email_status = json.loads(data)                    
            else:
                #存在则从数据库数据中中取出json数据
                email_status = json.loads(row[4])
            #从json数据中解析开关switch
            switch = email_status['send']['switch']
            if switch == "on":
                #判断邮件发送开关状态
                #解析json数据中的send_data
                next_send_date = email_status['send']['next_send_date']
                #解析已发送邮件次数
                send_times = email_status['send']['send_times']
                #读取配置文件中的下次发送时间，readconfig返回
                trigger_time = str(datetime.datetime.now().strftime(self.time_format))         
                #实例化发邮件函数
                email_managment = Email_managment()
                #设置时间格式
                time_format = '%Y-%m-%d %H:%M:%S'
                #将字符串转化为时间
                time_next_send_date = datetime.datetime.strptime(str(next_send_date), time_format)
                time_trigger_time = datetime.datetime.strptime(str(trigger_time), time_format)
                #判断数据库中某一行邮件状态中的下次发送时间是否   大于等于当前时间
                if time_next_send_date <= time_trigger_time:
                    logging.info(f'{datetime.datetime.now()}->时间检测成功，开始尝试发送邮件!')
                    print(f'符合发送条件，开始发送')
                    worker.signal.emit(f'符合发送条件，开始发送')
                    if not row[3]:
                    #给公邮发邮件 
                        template = get_email_template(send_times, company)
                        suject = template[0]
                        body = template[1]
                        status_sent = email_managment.send_email(
                            self.server,
                            self.port, 
                            self.username, 
                            self.password, 
                            self.username, 
                            email_info, 
                            suject,
                            body,
                            attachment=None
                            )
                        #如果发送成功则需要更新邮件发送状态
                        if status_sent:
                            current_time = datetime.datetime.now()
                            self.modfiy_email_status(                            
                                db_file,
                                id,
                                table_name,
                                send_times = int(send_times) + 1,
                                last_send_date = str(datetime.datetime.now().strftime(self.time_format)),
                                #下次发送时间
                                #get_send_time_gap()是根据邮件已发送次数判断间隔几天再发送
                                next_send_date = str((current_time + datetime.timedelta(days=get_send_time_gap(send_times))).strftime(self.time_format)),
                                error_times = 0,
                                switch = switch,
                                receive_times = 0,
                                last_receive_date = 0)
                            logging.info(f'{datetime.datetime.now()}->邮件发送成功!，公司{company}, 收件人{email_info}')
                            print(f'发送成功,收件人{email_info}，公司{company}')
                            worker.signal.emit(f'发送成功,收件人{email_info}，公司{company}')
                            time.sleep(90)
                            worker.signal.emit('95秒后处理下一条数据')
                        else:
                            print("邮件发送失败！")
                            worker.signal.emit(f'{datetime.datetime.now()}->邮件发送失败！->{status_sent}')
                            logging.info(f'{datetime.datetime.now()}->邮件发送失败！->{status_sent}')
                    else:
                        contacts = json.loads(row[3]) 
                        #给联系人发邮件
                        for name, info in contacts.items():
                            template = get_email_template(send_times, name)
                            suject = template[0]
                            body = template[1]
                            status_sent = email_managment.send_email(
                                self.server,
                                self.port, 
                                self.username, 
                                self.password, 
                                self.username, 
                                info['email'], 
                                suject,
                                body,
                                attachment=None
                                )
                            if status_sent:
                                receiver = info['email']
                                logging.info(f'{datetime.datetime.now()}->邮件发送成功!，公司{company}, 收件人{receiver}')
                                current_time = datetime.datetime.now()
                                self.modfiy_email_status(                            
                                    db_file,
                                    id,
                                    table_name,
                                    send_times = int(send_times) + 1,
                                    last_send_date = str(datetime.datetime.now().strftime(self.time_format)),
                                    #下次发送时间
                                    next_send_date = str((current_time + datetime.timedelta(days=get_send_time_gap(send_times))).strftime(self.time_format)),
                                    error_times = 0,
                                    switch = switch,
                                    receive_times = 0,
                                    last_receive_date = 0)
                                receiver = info['email']
                                print(f'发送成功,收件人{receiver}，公司{company}')
                                print(f'{90+3+2}秒后处理下一条数据')
                                worker.signal.emit(f'发送成功,收件人{receiver}，公司{company}')
                                worker.signal.emit(f'{95}秒后处理下一条数据')
                                time.sleep(90)
                            else:
                                print("发送失败")
                                logging.info(f'{datetime.datetime.now()}->邮件发送失败！->{status_sent}')
                                worker.signal.emit(f'{datetime.datetime.now()}->邮件发送失败！->\t 邮件发送状态：{status_sent}')

                else:
                    print("未到预计发送时间！")
                    worker.signal.emit("未到预计发送时间！")

            time.sleep(3)

        

    #判断下email_status中的switch的开关状态
    def check_email_status_switch(email_status):
        switch = email_status['send']['switch']
        if switch:
            return switch
        else:
            return False
    '''
    #读取配置文件中邮件服务器相关信息
    def read_email_info_config(self):
        if not os.path.exists('config.ini'):
            #self.write()
            #return 
            print("配置文件不存在")
            return False
        else:
            config = configparser.ConfigParser()
            config.read('config.ini', encoding = 'utf-8')
            server = config.get('stmp_info','server')
            port = config.get('stmp_info','port')
            username = config.get('stmp_info','username')
            password = config.get('stmp_info','password')
            if server and port and username and password:
                return server, port, username, password
            else:
                print("邮件信息读取错误")
                return False
    '''

    #更新数据库中的eamil_status字段
    def modfiy_email_status(self,
                            db_file,
                            id,
                            table_name,
                            send_times,
                            last_send_date,
                            next_send_date,
                            error_times,
                            switch,
                            receive_times,
                            last_receive_date):

        # 连接到SQLite数据库
        conn = sqlite3.connect(db_file)
        # 创建游标对象
        cur = conn.cursor()
        # 准备要插入的数据
        data = {
            "send": {
                "send_times": send_times,
                "last_send_date": last_send_date,
                "next_send_date": next_send_date,
                "error_times": error_times,
                "switch":switch
                    },
            "receive": {
                "receive_times": receive_times,
                "last_receive_date": last_receive_date
                    }
                    }

        json_data = json.dumps(data)
        # 将数据插入到数据库中
        conn.execute(
            f"UPDATE {table_name} SET email_status = ? WHERE id = ?",
            [json_data, id]
        )
                # 关闭游标和连接
        conn.commit()
        cur.close()
        conn.close()
        print(f'更新了数据库{id}')
    
'''
#测试用
main = Start_send()
db_file = 'test.db'
table_name = 'test'
main.start_send(db_file, table_name)
'''