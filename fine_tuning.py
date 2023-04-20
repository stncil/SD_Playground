import requests, sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap, QPalette, QColor, QMovie
from PyQt5.QtCore import Qt


from utils import url, button_style, imagebox_style


class FinetuneTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.setGeometry(100, 20, 250, 40)
        self.textbox.setPlaceholderText('Write your prompt here')
        self.textbox.setStyleSheet(
            "font-size: 16px; background-color: #f2f2f2; border: 2px solid #bfbfbf; border-radius: 20px; padding: 10px;")

        self.button = QtWidgets.QPushButton('Select training images', self)
        self.button.clicked.connect(self.showFileDialog)
        self.button.setStyleSheet(button_style)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.textbox)
        self.setLayout(layout)
        self.movie = QMovie("./loading.gif")
        self.imagebox = QtWidgets.QLabel()
        self.imagebox.setAlignment(Qt.AlignCenter)
        self.imagebox.setStyleSheet(imagebox_style)
        self.diff_button = QtWidgets.QPushButton('Run Diffusion', self)
        self.diff_button.clicked.connect(self.run_diffusion)
        self.diff_button.setStyleSheet(button_style)

        layout.addWidget(self.imagebox)
        layout.addWidget(self.diff_button)

    def showFileDialog(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        self.imagebox.setMovie(self.movie)
        self.movie.start()

        if file_dialog.exec_():
            # Get the selected file paths

            file_paths = file_dialog.selectedFiles()
            files = []

            for file_path in file_paths:
                print(file_path)
                file_name = file_path.split("/")[-1]
                files.append((file_name[:-4], (file_name, open(file_path, "rb"),
                                               "image/"+file_name[file_name.find(".")+1:])))
            print(files)
            response = requests.post(url+'/dreambooth', files=files)
            print(response.content)

    def run_diffusion(self):
        response = requests.post(url+'/dreambooth_inference')
        print(response.content)
        if response.status_code == 200:
            with open("./response.jpg", 'wb') as f:
                f.write(response.content)
        pixmap = QtGui.QPixmap("./response.jpg")
        self.imagebox.setPixmap(pixmap)
        self.imagebox.resize(pixmap.width(), pixmap.height())
        self.imagebox.show()

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 800)
        self.setWindowTitle('Tabs Example')
        tab_widget = QtWidgets.QTabWidget(self)
        tab_widget.addTab(FinetuneTab(), 'File')
        self.setCentralWidget(tab_widget)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
