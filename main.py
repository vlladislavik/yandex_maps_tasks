import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5 import Qt, QtGui, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
# from ui_file import Ui_MainWindow

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):  # Ui_MainWindow
    def __init__(self):
        super().__init__()
        uic.loadUi('yandex_maps.ui', self)
        # self.setupUi(self)
        # self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.btn.clicked.connect(self.getImage)

    def getImage(self):
        self.spn = list(map(lambda i: int(float(i) * 100), self.spn_pole.toPlainText().split(', ')))
        self.coords = self.coords_pole.toPlainText().split(', ')

        print(self.coords, self.spn)

        map_request = (f"http://static-maps.yandex.ru/1.x/?ll={self.coords[1]},{self.coords[0]}"
                       f"&spn={self.spn[0] / 100},{self.spn[1] / 100}&l=map")
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.map_image.setPixmap(self.pixmap)
        '''self.spn_pole.setReadOnly(True)
        self.coords_pole.setReadOnly(True)'''

    def keyPressEvent(self, event) -> None:
        if event.key() == QtCore.Qt.Key_PageUp:
            if self.spn[0] < 15:
                self.spn[0] += 5
                self.spn[1] += 5
            else:
                self.spn[0] += 50
                self.spn[1] += 50
            self.spn_pole.setText(f'{self.spn[0] / 100}, {self.spn[1] / 100}')
            self.getImage()
        elif event.key() == QtCore.Qt.Key_PageDown:
            if self.spn[0] < 15:
                self.spn[0] -= 5
                self.spn[1] -= 5
            else:
                self.spn[0] -= 50
                self.spn[1] -= 50
            self.spn_pole.setText(f'{self.spn[0] / 100}, {self.spn[1] / 100}')
            print(self.spn)
            self.getImage()

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
