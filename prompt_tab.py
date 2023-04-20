import requests
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap, QPalette, QColor, QMovie
from PyQt5.QtCore import Qt


from utils import url, button_style, imagebox_style, Tab_StyleSheet



class PromptTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(Tab_StyleSheet)

        self.movie = QMovie("loading.gif")

        # Create text input box
        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.setGeometry(100, 20, 250, 40)
        self.textbox.setPlaceholderText('Write your prompt here')
        self.textbox.setStyleSheet(
            "font-size: 16px; background-color: #f2f2f2; border: 2px solid #bfbfbf; border-radius: 20px; padding: 10px;")

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
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.imagebox)
        self.layout.addWidget(self.button, alignment=Qt.AlignBottom)

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
        movie = QMovie('loading.gif')
        self.imagebox.setMovie(movie)
        movie.start()

        response = requests.post(url + "/text_prompt", files={'image': open('./temp_image.jpg', 'rb')},
                                 data={'text': self.textbox.text()})
        if response.status_code == 200:
            with open("./temp_image_out.jpg", 'wb') as f:
                f.write(response.content)
            pixmap = QtGui.QPixmap("./temp_image_out.jpg")
            self.imagebox.setPixmap(pixmap)
            self.imagebox.resize(pixmap.width(), pixmap.height())
            self.imagebox.show()
