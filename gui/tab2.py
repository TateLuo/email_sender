from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QFileDialog, QMessageBox, QComboBox, QColorDialog, QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from bs4 import BeautifulSoup
import sys,re, os

class Tab2(QWidget):
    def __init__(self):
        super().__init__()
        self.fileName = None
        # 添加一个标志来记录文本是否被修改过
        self.isTextChanged = False  
        self.initUI()
    
    #初始化
    def initUI(self):
        self.setWindowTitle('HTML内容编辑器')
        self.saveButton = QPushButton('保存')
        self.saveButton.clicked.connect(self.saveContent)
        self.fontSizeComboBox = QComboBox()
        self.fontSizeComboBox.addItems([str(i) for i in range(6,73,2)])
        self.fontSizeComboBox.currentTextChanged.connect(self.changeFontSize)
        self.boldButton = QPushButton('加粗')
        self.boldButton.clicked.connect(self.boldText)
        self.fontComboBox = QComboBox()
        self.fontComboBox.addItems(['Arial', 'Verdana', 'Helvetica', 'Tahoma', 'Trebuchet MS', 'Times New Roman', 'Georgia', 'Garamond', 'Courier New', 'Brush Script MT'])
        self.fontComboBox.currentTextChanged.connect(self.changeFontFamily)
        self.fontColorButton = QPushButton('选择字体颜色')
        self.fontColorButton.clicked.connect(self.changeFontColor)
        self.alignLeftButton = QPushButton('左对齐')
        self.alignLeftButton.clicked.connect(lambda: self.textEdit.setAlignment(Qt.AlignLeft))
        self.alignCenterButton = QPushButton('居中')
        self.alignCenterButton.clicked.connect(lambda: self.textEdit.setAlignment(Qt.AlignCenter))
        self.alignRightButton = QPushButton('右对齐')
        self.alignRightButton.clicked.connect(lambda: self.textEdit.setAlignment(Qt.AlignRight))
        self.textEdit = QTextEdit()
        self.textEdit.cursorPositionChanged.connect(self.cursorPositionChanged)
        self.main_layout = QHBoxLayout()
        self.layout = QVBoxLayout()
        self.toolbarLayout = QHBoxLayout()
        self.toolbarLayout.addWidget(self.saveButton)
        self.toolbarLayout.addWidget(self.fontSizeComboBox)
        self.toolbarLayout.addWidget(self.boldButton)
        self.toolbarLayout.addWidget(self.fontComboBox)
        self.toolbarLayout.addWidget(self.fontColorButton)
        self.toolbarLayout.addWidget(self.alignLeftButton)
        self.toolbarLayout.addWidget(self.alignCenterButton)
        self.toolbarLayout.addWidget(self.alignRightButton)
        self.layout.addLayout(self.toolbarLayout)
        self.layout.addWidget(self.textEdit)
         # 创建一个QListWidget
        self.fileListWidget = QListWidget()
        # 获取templates文件夹中的所有HTML文件
        # 获取当前模块的绝对路径
        current_path = os.path.dirname(os.path.abspath(__file__))
        # 获取主目录（也就是当前目录的上一级目录）
        main_directory = os.path.dirname(current_path)
        templates_dir = os.path.join(main_directory, 'templates')
        html_files = [f for f in os.listdir(templates_dir) if f.endswith('.html')]
        # 将HTML文件添加到列表中
        self.fileListWidget.addItems(html_files)
        # 设置列表部件的宽度
        self.fileListWidget.setMaximumWidth(200)
        # 连接itemClicked信号到槽
        self.fileListWidget.itemClicked.connect(self.openFileFromList)
        self.textEdit.textChanged.connect(self.textChanged)  # 连接textChanged信号到槽
        # 将列表添加到布局中
        self.main_layout.addWidget(self.fileListWidget)
        self.main_layout.addLayout(self.layout)
        self.setLayout(self.main_layout)
    
    # 当文本发生改变时，设置标志为True   
    def textChanged(self):
        self.isTextChanged = True   

    #打开html文件内容，会将变量暂时替换为{{name}}这种形式，便于查看
    def openFile(self):
        if not self.fileName:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self,"打开HTML文件", "","HTML Files (*.html)", options=options)
            if fileName:
                self.fileName = fileName
        with open(self.fileName, 'r', encoding='utf-8') as f:
            html_content = f.read()
            # Use regular expressions to find comments and replace them with the content inside the comments
            html_content = re.sub(r'<!-- (.*?) -->(.*?)<!-- /(.*?) -->', r'<b>{{\2}}</b>', html_content)
            self.textEdit.setHtml(html_content)
                # 添加一个标志来记录文本是否被修改过
        self.isTextChanged = False
    
    #保存编辑区域内容
    def saveContent(self):
        if self.fileName and self.isTextChanged:
            reply = QMessageBox.question(self, '保存', '是否保存修改？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                htmlContent = self.textEdit.toHtml()
                # Use regular expressions to remove the bold tags and add comments back to the content
                htmlContent = re.sub(r'{{(.*?)}}', lambda match: '<!-- {} -->{}<!-- /{} -->'.format(match.group(1).upper(), match.group(1), match.group(1).upper()), htmlContent)
                with open(self.fileName, 'w', encoding='utf-8') as f:
                    f.write(htmlContent)
                print(f'内容已保存到文件：{self.fileName}')  
            self.isTextChanged = False  # 保存文件后，重置标志为False
        elif self.isTextChanged:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self,"保存文件","","HTMLFiles(*.html)",options=options)
            if fileName:
                self.fileName = fileName
                htmlContent = self.textEdit.toHtml()
                # Use regular expressions to remove the bold tags and add comments back to the content
                htmlContent = re.sub(r'{{(.*?)}}', lambda match: '<!-- {} -->{}<!-- /{} -->'.format(match.group(1).upper(), match.group(1), match.group(1).upper()), htmlContent)
                with open(self.fileName, 'w', encoding='utf-8') as f:
                    f.write(htmlContent)
                print(f'内容已保存到文件：{self.fileName}')  
            else:
                print('请先打开一个文件。')
            self.isTextChanged = False  # 保存文件后，重置标志为False
            
    
    #选中模板列表事件
    def openFileFromList(self, item):
        print(self.textEdit.toPlainText().strip().replace(" ", "").replace("\n", "").replace("\r", ""))
        # 检查编辑区域是否为空
        text = self.textEdit.toPlainText()
        if ''.join(filter(str.isprintable, text)):
        # 如果不为空，则保存内容
            self.saveContent()
        current_path = os.path.dirname(os.path.abspath(__file__))
        # 获取主目录（也就是当前目录的上一级目录）
        main_directory = os.path.dirname(current_path)
        # 打开选中的文件
        self.fileName = os.path.join(main_directory, 'templates', item.text())
        self.openFile()
    
    #修改文字大小
    def changeFontSize(self, size):
        self.textEdit.setFontPointSize(float(size))
    
    #加粗
    def boldText(self):
        if self.textEdit.fontWeight() == QFont.Bold:
            self.textEdit.setFontWeight(QFont.Normal)
        else:
            self.textEdit.setFontWeight(QFont.Bold)
    
    #修改字体
    def changeFontFamily(self, family):
        self.textEdit.setCurrentFont(QFont(family))


    
    #修改字体颜色
    def changeFontColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.textEdit.setTextColor(color)
            self.fontColorButton.setStyleSheet(f'color: {color};')
    
        
    #光标选中时
    def cursorPositionChanged(self):
        #先将下拉选选框设置成可编辑
        self.fontComboBox.setEditable(True)
        self.fontSizeComboBox.setEditable(True)
        format = self.textEdit.textCursor().charFormat()
        
        #检测当前选中文字是否为粗体，若是则将粗体按钮设置为粗体
        if format.fontWeight() == QFont.Bold:
            self.boldButton.setStyleSheet("font: bold;")
        else:
            self.boldButton.setStyleSheet("font: normal;")
        
        #显示当前选中字体颜色
        color = format.foreground().color().name()
        self.fontColorButton.setStyleSheet(f'color: {color};')
        
        #显示当前字号字体
        self.fontSizeComboBox.setCurrentText(str(int(format.fontPointSize())))
        self.fontComboBox.setCurrentText(format.fontFamily())
        
            # 获取当前选中文字的对齐方式
        alignment = self.textEdit.textCursor().blockFormat().alignment()
        if alignment & Qt.AlignLeft:
            self.alignLeftButton.setStyleSheet("font: bold;")
            self.alignRightButton.setStyleSheet("font: normal;")
            self.alignCenterButton.setStyleSheet("font: normal;")
        elif alignment & Qt.AlignRight:
            self.alignRightButton.setStyleSheet("font: bold;")
            self.alignLeftButton.setStyleSheet("font: normal;")
            self.alignCenterButton.setStyleSheet("font: normal;")
        elif alignment & Qt.AlignCenter:
            self.alignCenterButton.setStyleSheet("font: bold;")
            self.alignRightButton.setStyleSheet("font: normal;")
            self.alignLeftButton.setStyleSheet("font: normal;")
        elif alignment & Qt.AlignJustify:
            print('文字是两端对齐的')