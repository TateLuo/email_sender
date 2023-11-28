from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox
import configparser, os

class ConfigEditor(QWidget):
    def __init__(self):
        super().__init__()
        # 获取template目录的路径
        current_path = os.path.dirname(os.path.abspath(__file__))
        # 获取主目录（也就是当前目录的上一级目录）
        main_directory = os.path.dirname(current_path)
        self.config = configparser.ConfigParser()
        self.config.read(main_directory+'/config.ini')

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        self.labels = {}
        self.lineEdits = {}

        for section in self.config.sections():
            for key in self.config[section]:
                self.labels[key] = QLabel(f'{section} - {key}', self)
                self.lineEdits[key] = QLineEdit(self)
                self.lineEdits[key].setText(self.config[section][key])
                vbox.addWidget(self.labels[key])
                vbox.addWidget(self.lineEdits[key])
                print("遍历到了key"+key)
        self.btn = QPushButton('Save', self)
        self.btn.clicked.connect(self.saveConfig)
        vbox.addWidget(self.btn)

    def saveConfig(self):
        reply = QMessageBox.question(self, '保存', '是否保存修改？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for section in self.config.sections():
                for key in self.config[section]:
                    self.config[section][key] = self.lineEdits[key].text()

            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
