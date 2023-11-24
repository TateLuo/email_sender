import os, configparser, sys
from start_send import Start_send
import schedule
import time
import logging
import traceback


class Main:
    def __init__(self):
        self.schedule_send_times()

    #读取配置文件中数据库的信息
    def read_config_database(self):
        # 获取程序所在目录的路径
        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        if not os.path.exists(dir_path+"\\config.ini"):
            return False
        else:
            config = configparser.ConfigParser()
            config.read(dir_path+'\\config.ini', encoding = 'utf-8')
            db_name = config.get('database','db_name')
            table_name = config.get('database', 'table_name').split(',')
            return db_name, table_name
    
    #读取配置文件中关于邮件发送间隔的配置信息
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
    
    def schedule_send_times(self):
        #print(self.send_email_gap_info())
        # 获取配置项的值，并根据逗号分隔符拆分为列表
        execution_times  = self.send_email_gap_info()
        # 根据配置文件中的时间设置定时任务
        for execution_time in execution_times:
            schedule.every().day.at(execution_time.strip()).do(self.work_start)
    
    #开始干活
    def work_start(self):
        start_email = Start_send()
        database_info =  self.read_config_database()
        db_name = database_info[0]
        table_name = database_info[1]
        for item in table_name:
            print(f'开始处理数据库{item}')
            start_email.start_send(db_name,item)      


# 获取程序所在目录的路径
dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))

# 定义日志文件的路径
log_file = os.path.join(dir_path, 'log.txt')

# 配置日志
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
i=1
while True:
    i = i + 1 
    logging.info('程序运行'+ str(i+1) +'次', exc_info=True)
    try:
        print("\n\n邮件程序正在运行...........")
        main = Main()
        main.work_start()
        #schedule.run_pending()
        time.sleep(2)
    except Exception as e:
        print("\n发生异常:", str(e))
        logging.error(str(e), exc_info=True)
        traceback.print_exc()