import configparser
import os, sys

class ConfigTool:
    def __init__(self):
        # 获取程序所在目录的路径
        self.dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.config = configparser.ConfigParser()
        self.config.read(self.dir_path+'/config.ini', encoding = 'utf-8')


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
