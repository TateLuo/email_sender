import sys, os
from PyQt5.QtWidgets import QApplication
from gui.my_app import MyApp
from PyQt5.QtGui import QIcon
from qq import img
import base64



def set_icon(QApplication):
    
    print("开始设置图标")
    # 将import进来的icon.py里的数据转换成临时文件tmp.ico，作为图标
    tmp = open("tmp.ico","wb+")  
    tmp.write(base64.b64decode(img))#写入到临时文件中
    tmp.close()
    app_icon = QIcon("tmp.ico")
    QApplication.setWindowIcon(app_icon) #设置图标
    os.remove("tmp.ico")



if __name__ == '__main__':

    app = QApplication(sys.argv)

    set_icon(QApplication)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
    
        #设置图标
