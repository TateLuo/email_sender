import configparser
import os, sys


class ConfigTool:
    def __init__(self):
        # 获取程序所在目录的路径
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.config = configparser.ConfigParser()
        #拼接配置文件路径
        self.config_path = os.path.join(self.dir_path,"config.ini")
        #d读取配置文件
        self.config.read(self.config_path, encoding = 'utf-8')


    #从配置文件获取发信者的信息
    def get_userinfo(self):
        username = self.config.get("user_info","username")
        position = self.config.get("user_info","position")
        company = self.config.get("user_info","company")
        return username, position, company
    
    #从配置文件获取自定义模板中需要增加的字段列表
    def get_customize_variable(self):
        customize_variable = self.config.get("user_info","customize_variable")
        return customize_variable

    #获取发信时间间隔，数组位置对应发信阶段
    def get_time_gap(self):
        time_gap = self.config.get("stage_info","time_gap")
        return time_gap

    #读取配置文件中stmp邮件服务器相关信息
    def read_email_info_config(self):
        #print(self.config_path)
        if not os.path.exists(self.config_path):
            #self.write()
            #return 
            print("配置文件不存在")
            return False
        else:
            server = self.config.get('stmp_info','server')
            port = self.config.get('stmp_info','port')
            username = self.config.get('stmp_info','username')
            password = self.config.get('stmp_info','password')
            if server and port and username and password:
                return server, port, username, password
            else:
                print("邮件信息读取错误")
                return False
    
    #读取配置文件中的数据库名和表名信息
    def read_config_database(self):
        if not os.path.exists(self.config_path):
            return False
        else:
            self.config.read(self.config_path, encoding = 'utf-8')
            db_name = self.config.get('database','db_name')
            table_name = self.config.get('database', 'table_name').split(',')
            return db_name, table_name