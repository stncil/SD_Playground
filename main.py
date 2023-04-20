import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap, QPalette, QColor, QMovie
from PyQt5.QtCore import Qt
from painting_tab import PaintTab
from prompt_tab import PromptTab
from fine_tuning import FinetuneTab
from guidance_process import guidance_tab

from utils import imagebox_style_2, button_style, Tab_StyleSheet

class GreetingPopup(QtWidgets.QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Greetings")
        self.setWindowIcon(QtGui.QIcon('photoshop.ico'))

        self.setGeometry(100, 100, 400, 200)

        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        layout = QtWidgets.QVBoxLayout()

        greeting = QtWidgets.QLabel(f"Hello {self.name}!")
        greeting.setStyleSheet(imagebox_style_2)

        ok_button = QtWidgets.QPushButton("OK")
        ok_button.setStyleSheet(button_style)
        ok_button.clicked.connect(self.close)

        layout.addWidget(greeting)
        layout.addWidget(ok_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 800)
        self.setWindowTitle('Adobe Diffusion')
        tab_widget = QtWidgets.QTabWidget(self)
        tab_widget.setStyleSheet(Tab_StyleSheet)
        tab_widget.addTab(PromptTab(), 'Simple Prompt')
        tab_widget.addTab(PaintTab(), 'Paint and Diffuse')
        tab_widget.addTab(FinetuneTab(), 'Dreambooth')
        tab_widget.addTab(guidance_tab(), 'More Guidance')
        self.setCentralWidget(tab_widget)

        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.show()


app = QtWidgets.QApplication(sys.argv)
popup = GreetingPopup("Create Diffusion Images")

window = MainWindow()
favicon = QtGui.QIcon('./photoshop.ico')
window.setWindowIcon(favicon)
window.show()
popup.show()
app.exec_()

