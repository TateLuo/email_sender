import configparser
from config_tool import ConfigTool
import os, sys, json
import traceback

#获取邮件模板
#输入参数send_times-发信次数
#输入参数name-客户名称
def get_email_template(send_times, name):
    send_times = int(send_times)
    configTool = ConfigTool()
    #获取发送间隔次数长度
    time_gap_list = configTool.get_time_gap().split(',')
    #获取当前运行程序根目录
    dir_path = os.path.dirname(os.path.abspath(__file__))
    #拼接模板文件夹地址
    templates_path = os.path.join(dir_path,"templates\\")
    #根据发送次数获取模板
    #但是如果发送次数已经大于自己设定的最大发送数，就默认发送over模板
    template_index = send_times
    if send_times >= len(time_gap_list):
        template_index = 'over'    
    template = templates_path + f'{template_index}.html'
    try:
        if os.path.exists(template):
            with open(template, 'r') as file:
                placeholder = "SUBJECT"
                #读取html模板
                tmp_template_content = file.read()
                #替换变量
                template_content = replace_cus_string_in_html(tmp_template_content, send_times, name)
                final_html = template_content[0]
                subject = template_content[1]
                #返回标题和无标题已替换变量模板
                return subject, final_html
        else:
            with open(templates_path+'erro.html', 'r') as file:
                placeholder = "SUBJECT"
                tmp_template_content = file.read()
                subject = extract_string_from_html(tmp_template_content, placeholder)[0]
                tmp_template_without_subject = extract_string_from_html(tmp_template_content, placeholder)[1]
                template_content = replace_cus_string_in_html(tmp_template_without_subject,"erro", name)
                #template_content = replace_string_in_html(tmp_template_content, subject, placeholder, name)
                return subject, template_content
    except:
        print('读取模板文件出错！')
        traceback.print_exc()
                
#获取发信间隔
#根据配置文件中的设置计算
#输入参数send_times-发信次数
def get_send_time_gap(send_times):
    send_times = int(send_times)
    configTool = ConfigTool()
    time_gap_list = configTool.get_time_gap().split(',')
    if len(time_gap_list) >= send_times:
        return int(time_gap_list[send_times-1])
    else:
        return int(time_gap_list[len(time_gap_list)-1])


#读取配置文件中自定义变量并替换html中的占位符
#同时取出配置文件中的标题（subject）
#输入参数html-html模板
#输入参数send_times-发信次数
#输入参数name-客户名称
def replace_cus_string_in_html(html, send_times, name):
    configTool = ConfigTool()
    #获取所有模板的自定义变量
    variable_templates = json.loads(configTool.get_customize_variable())

    #根据发送次数获取具体对应模板的自定义变量,不存则则直接取用erro模板
    if not str(send_times) in str(variable_templates):
        list_variable = list_variable = variable_templates["erro"]
    else:    
        list_variable = variable_templates[str(send_times)]
    #把客户名也添加进列表，占位词是customername
    name = {"customername":name}
    list_variable.update(name)
    #获取json数据中的所有键，并设为一个列表
    key_marker = list(list_variable.keys())
    #获取json数据中所有值，并设为一个列表
    value_marker = list(list_variable.values())
    #初始化标题
    subject = ""
    for i in range(len(key_marker)):
        if not "subject"== key_marker[i]:
            #占位符
            placeholder = (key_marker[i]).upper()
            # 将整个 HTML 的内容替换掉占位符和提取的字符串
            start_marker = f"<!-- {placeholder} -->"
            end_marker = f"<!-- /{placeholder} -->"
            html = html.replace(start_marker + key_marker[i] + end_marker, value_marker[i])
            html = html.replace("\n","")
            #print(f'本次替换{start_marker + key_marker[i] + end_marker, value_marker[i]}')
        else:
            subject =  value_marker[i]
            #占位符
            placeholder = (key_marker[i]).upper()
            # 将整个 HTML 的内容替换掉占位符和提取的字符串
            start_marker = f"<!-- {placeholder} -->"
            end_marker = f"<!-- /{placeholder} -->"
            html = html.replace(start_marker + key_marker[i] + end_marker, "")
            html = html.replace("\n","")
    return html, subject