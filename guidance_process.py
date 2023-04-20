import requests, sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap, QPalette, QColor, QMovie
from PyQt5.QtCore import Qt


from utils import url, button_style, imagebox_style



class guidance_tab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # self.setGeometry(100, 100, 500, 600)

        self.movie = QMovie("loading.gif")
        hbox = QtWidgets.QHBoxLayout()

        self.checkbox = QtWidgets.QCheckBox("Flip Switch")

        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setValue(50)
        slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        slider.setTickInterval(10)


        # Create text input box
        self.textbox = QtWidgets.QTextEdit()
        self.textbox.setFixedHeight(100)
        self.textbox.setPlaceholderText('Write your prompt here')
        self.textbox.setStyleSheet(
            "font-size: 16px; background-color: #f2f2f2; border: 2px solid #bfbfbf; border-radius: 20px; padding: 10px;")

        self.codebox = QtWidgets.QTextEdit()
        self.codebox.setFixedHeight(100)
        self.codebox.setPlaceholderText('Loss func code')
        self.codebox.setStyleSheet(
            "font-size: 16px; background-color: #f2f2f2; border: 2px solid #bfbfbf; border-radius: 20px; padding: 10px;")

        hbox.addWidget(self.textbox)
        hbox.addWidget(self.codebox)
        hbox.addWidget(self.checkbox)
        # Create image display box
        self.imagebox = QtWidgets.QLabel(self)
        self.imagebox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.imagebox.setAlignment(Qt.AlignCenter)
        self.imagebox.setStyleSheet(imagebox_style)

        # Create select file button
        self.button = QtWidgets.QPushButton("Run Diffusion", self)
        self.button.clicked.connect(self.run_diffusion)
        self.button.setCheckable(True)
        self.button.setGeometry(20, 500, 100, 40)
        self.button.setStyleSheet(button_style)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(hbox)
        self.layout.addWidget(slider)
        self.layout.addWidget(self.imagebox)
        self.layout.addWidget(self.button, alignment=Qt.AlignBottom)
        self.setLayout(self.layout)

    def select_file(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", "",
                                                   "Image Files (*.png *.jpg)", options=options)
        if file_path:
            # If a file was selected, set the file path to the label and load the image
            pixmap = QPixmap(file_path)
            self.imagebox.setPixmap(pixmap)
            self.imagebox.resize(pixmap.width(), pixmap.height())
            self.imagebox.show()

    def run_diffusion(self):
        if self.checkbox.isChecked():
            print(self.codebox.toPlainText())
            print(self.textbox.toPlainText())

        response = requests.post(url + "/guidance", data={'text': self.textbox.toPlainText(),\
                                                          'code': self.codebox.toPlainText()})
        if response.status_code == 200:
            with open("./temp_image_out.jpg", 'wb') as f:
                f.write(response.content)
            pixmap = QtGui.QPixmap("./temp_image_out.jpg")
            self.imagebox.setPixmap(pixmap)
            self.imagebox.resize(pixmap.width(), pixmap.height())
            self.imagebox.show()

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 800)
        self.setWindowTitle('Tabs Example')
        tab_widget = QtWidgets.QTabWidget(self)
        tab_widget.addTab(guidance_tab(), 'Guidance_tab')
        self.setCentralWidget(tab_widget)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()