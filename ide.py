import sys
from PyQt5.QtGui import QFont, QFontDatabase, QColor, QSyntaxHighlighter, QTextCharFormat, QIcon
import time
import re
from PyQt5.QtWidgets import *				    
from PyQt5.QtCore import Qt
from threading import *

class Highlighter(QSyntaxHighlighter):
	def __init__(self, parent=None):
		super().__init__(parent)
		self._mapping = {}

	def add_mapping(self, pattern, pattern_format):
		self._mapping[pattern] = pattern_format

	def highlightBlock(self, text_block):
		for pattern, fmt in self._mapping.items():
			for match in re.finditer(pattern, text_block):
				start, end = match.span()
				self.setFormat(start, end-start, fmt)

class Window(QMainWindow):
	def __init__(self):
		super().__init__()

		# set the title of main window
		self.setWindowTitle('Prog Bits custom ide')

		# set the size of window
		self.Width = 800
		self.height = int(0.618 * self.Width)
		self.resize(self.Width, self.height)
		self.highlighter = Highlighter()
		self.setUpEditor()
		# add all widgets
		self.btn_1 = QPushButton('Save', self)
		self.btn_2 = QPushButton('Open file', self)
	

		self.btn_1.clicked.connect(self.button1)
		self.btn_2.clicked.connect(self.button2)
		self.l = QListWidget()
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)
		self.layout.addWidget(self.editor)
		# add tabs
		self.tab1 = self.ui1()
		self.tab2 = self.ui2()
		self.tab3 = self.ui3()
		self.thread()
		self.initUI()
	def setUpEditor(self): #setting up text editor and highlighter
		#highlight class
		class_format = QTextCharFormat()
		class_format.setForeground(Qt.blue)
		class_format.setFontWeight(QFont.Bold)
		class_format.setFontPointSize(4000)
		pattern = r'^\s*class\s+\w+\(.*$'
		self.highlighter.add_mapping(pattern, class_format)

		#highlight words like print, if, else etc.
		function_format = QTextCharFormat()
		function_format.setForeground(Qt.red)
		function_format.setFontItalic(True)
		pattern = "\\bprint\\b"
		self.highlighter.add_mapping(pattern, function_format)

		#highlight any word between ""
		
		function_format = QTextCharFormat()
		function_format.setForeground(Qt.green)
		function_format.setFontItalic(True)
		pattern = r'"\w+\"'
		self.highlighter.add_mapping(pattern, function_format)      

		#highlight # symbol
		comment_format = QTextCharFormat()
		comment_format.setBackground(QColor("#77ff77"))
		pattern = r'#.*$'
		self.highlighter.add_mapping(pattern, comment_format)

		self.editor = QPlainTextEdit()
		self.editor.setStyleSheet("color: white; background-color: black;")
		
		font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
		font.setPointSize(16)
		self.editor.setFont(font)

		self.highlighter.setDocument(self.editor.document())
	
	def Operation(self): #openfile
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			
			f = open(fileName, "r")
			print(fileName)
			self.editor.clear()
			self.editor.insertPlainText(f.read())
	def Operation2(self, location): #savefile
		
		file = open(location,'w')
		text = self.editor.toPlainText()
		file.write(text)
		file.close()
	def initUI(self): #setup ui (adding buttons and tabs)
		left_layout = QVBoxLayout()
		left_layout.addWidget(self.btn_1)
		left_layout.addWidget(self.btn_2)
		
		

		left_layout.addStretch(5)
		left_layout.setSpacing(20)
		left_widget = QWidget()
		left_widget.setLayout(left_layout)

		self.right_widget = QTabWidget()
		self.right_widget.tabBar().setObjectName("mainTab")

		self.right_widget.addTab(self.tab1, '')
		self.right_widget.addTab(self.tab2, '')
		self.right_widget.addTab(self.tab3, '')

		self.right_widget.setCurrentIndex(0)
		self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
			height: 0; margin: 0; padding: 0; border: none;}''')

		main_layout = QHBoxLayout()
		main_layout.addWidget(left_widget)
		main_layout.addWidget(self.editor)
		
		main_layout.setStretch(0, 40)
		main_layout.setStretch(1, 200)
		main_widget = QWidget()
		main_widget.setLayout(main_layout)
		self.setCentralWidget(main_widget)
		

	# ----------------- 
	# buttons
 
	def button1(self): #save file
		name = QFileDialog.getSaveFileName(self, 'Save File')
		f = open(name[0], "w")
		f.write(self.editor.toPlainText())
		f.close()
	def button2(self):
		
		t1=Thread(target=self.Operation)
		t1.start()
	

	# ----------------- 
	# pages

	def ui1(self):
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self.layout.addWidget(self.editor)
		main = QWidget()
		main.setLayout(self.layout)
		return main

	def ui2(self):
		main_layout = QVBoxLayout()
		main_layout.addWidget(QLabel('page 2'))
		main_layout.addStretch(5)
		main = QWidget()
		main.setLayout(main_layout)
		return main

	def ui3(self):
		
		self.layout = QHBoxLayout()
		self.setLayout(self.layout)
		self.layout.addWidget(self.editor)
		main = QWidget()
		main.setLayout(self.layout)
		return main

	


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Window()
	ex.show()
	sys.exit(app.exec_())
