import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('yandex_maps.ui', self)

        self.btn.clicked.connect(self.getImage)

    def getImage(self):
        self.spn = self.spn_pole.toPlainText().split(', ')
        self.coords = self.coords_pole.toPlainText().split(', ')

        print(self.coords, self.spn)

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


    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())