import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap, QPalette, QColor, QMovie
from PyQt5.QtCore import Qt

import requests, cv2
from PIL import Image
from io import BytesIO
import base64

from utils import url, button_style, COLORS, imagebox_style



class Canvas(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()

        pixmap = QtGui.QPixmap(600, 600)#QtGui.QPixmap("./api/testimage.png")
        pixmap.fill(Qt.white)
        self.mask_pixmap = pixmap.copy()
        self.mask_pixmap.fill(Qt.white)
        self.setPixmap(pixmap)

        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#000000')

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return  # Ignore the first time.

        painter = QtGui.QPainter(self.pixmap())
        painter2 = QtGui.QPainter(self.mask_pixmap)
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter2.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        painter2.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter2.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()
        self.show()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None


class QPaletteButton(QtWidgets.QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(24, 24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)


class PaintTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.movie = QMovie("loading.gif")

        self.files_select = QtWidgets.QPushButton('Select Initial File', self)
        self.files_select.clicked.connect(self.display_file)
        self.files_select.setStyleSheet(button_style)

        self.canvas = Canvas()
        self.canvas.setStyleSheet(imagebox_style)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.files_select)

        self.text_edit = QtWidgets.QTextEdit(self)
        # self.text_edit.setFixedSize(500, 60)
        self.text_edit.setStyleSheet(
            "font-size: 16px; background-color: #f2f2f2; border: 2px solid #bfbfbf; border-radius: 20px; padding: 10px;")
        self.text_edit.setPlaceholderText('Write your prompt here')
        layout.addWidget(self.text_edit)
        layout.addWidget(self.canvas)
        palette = QtWidgets.QHBoxLayout()
        self.add_palette_buttons(palette)
        layout.addLayout(palette)

        self.button = QtWidgets.QPushButton('Run Diffusion', self)
        self.button.clicked.connect(self.run_diffusion)
        self.button.setStyleSheet(button_style)

        layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        layout.addWidget(self.button, alignment=Qt.AlignHCenter)
        # layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        self.setLayout(layout)

    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.set_pen_color(c))
            layout.addWidget(b)

    def run_diffusion(self):
        # movie = QMovie('loading.gif')
        # self.canvas.setMovie(movie)
        # movie.start()

        print(self.canvas.pixmap().toImage().save("./temp_image.jpg"))
        img = cv2.imread("./temp_image.jpg")
        img = 255-img
        cv2.imwrite("./temp_image.jpg", img)

        response = requests.post(url+'/imgtoimgpipe', files={'image': open('./temp_image.jpg', 'rb')},
                                 data={'text': self.text_edit.toPlainText()})
        if response.status_code == 200:
            with open("./temp_image_out.jpg", 'wb') as f:
                f.write(response.content)
            pixmap = QPixmap("./temp_image_out.jpg")
            self.canvas.setPixmap(pixmap)
            self.canvas.resize(pixmap.width(), pixmap.height())
            self.canvas.show()

    def display_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select File", "",
                                                             "Image Files (*.png *.jpg)")
        if file_path:
            # If a file was selected, set the file path to the label and load the image
            pixmap = QPixmap(file_path)
            self.canvas.setPixmap(pixmap)
            self.canvas.resize(pixmap.width(), pixmap.height())
            self.canvas.show()

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 600, 800)
        self.setWindowTitle('Tabs Example')
        tab_widget = QtWidgets.QTabWidget(self)
        tab_widget.addTab(PaintTab(), 'Paint_tab')
        self.setCentralWidget(tab_widget)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()