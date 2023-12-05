from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox
import configparser, os

class ConfigEditor(QWidget):
    def __init__(self):
        super().__init__()
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.main_directory = os.path.dirname(current_path)
        self.config = configparser.ConfigParser()
        self.config.read(self.main_directory+'/config.ini')

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        self.labels = {}
        self.lineEdits = {}

        for section in self.config.sections():
            for key in self.config[section]:
                label_name = f'{section}-{key}'
                self.labels[label_name] = QLabel(f'{section} - {key}', self)
                self.lineEdits[label_name] = QLineEdit(self)
                self.lineEdits[label_name].setText(self.config[section][key])
                vbox.addWidget(self.labels[label_name])
                vbox.addWidget(self.lineEdits[label_name])

        self.btn = QPushButton('Save', self)
        self.btn.clicked.connect(self.saveConfig)
        vbox.addWidget(self.btn)
        self.setWindowTitle('编辑通用配置')  

    def saveConfig(self):
        reply = QMessageBox.question(self, '保存', '是否保存修改？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for section in self.config.sections():
                for key in self.config[section]:
                    label_name = f'{section}-{key}'
                    self.config[section][key] = self.lineEdits[label_name].text()

            with open(self.main_directory+'/config.ini', 'w') as configfile:
                self.config.write(configfile)
