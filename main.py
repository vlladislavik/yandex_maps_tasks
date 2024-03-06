import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('yandex_maps.ui', self)

        self.spn = None
        self.coords = None

        self.btn.clicked.connect(self.getImage)

    def getImage(self):
        self.spn = self.spn_pole.toPlainText().split(', ')
        self.coords = self.coords_pole.toPlainText().split(', ')

        print(self.coords, self.spn)

        self.show_map()

    def show_map(self):
        map_request = ("http://static-maps.yandex.ru/1.x/?ll={},{}"
                       "&spn={},{}&l=map").format(self.coords[1], self.coords[0],
                                                  self.spn[0], self.spn[1])
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spn = [int(self.spn[0]) + 0.02, int(self.spn[1]) + 0.02]
            print('pgup', self.spn)
            self.show_map()
        if event.key() == Qt.Key_PageDown:
            if not (int(self.spn[0]) - 0.02 < 0 or int(self.spn[1]) - 0.02 < 0):
                self.spn = [int(self.spn[0]) - 0.0002, int(self.spn[1]) - 0.0002]
                print('pgdn', self.spn)
                self.show_map()

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())