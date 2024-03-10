import os
import sys
import math

import requests
from PyQt5.QtGui import QPixmap
from PyQt5 import Qt, QtGui, QtCore, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
# from ui_file import Ui_MainWindow

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):  # Ui_MainWindow
    MAP_IS_ACTIVE = False
    def __init__(self):
        super().__init__()
        uic.loadUi('yandex_maps.ui', self)
        # self.setupUi(self)
        # self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.spn_pole.setText('90, 90')
        self.coords_pole.setText('0, 0')

        self.btn.clicked.connect(self.getImage)

        self.MapType = Qt.QButtonGroup(self)
        self.MapType.addButton(self.SchemMapType, 1)
        self.MapType.addButton(self.SputnikMapType, 2)
        self.MapType.addButton(self.HybridMapType, 3)
        # self.MapType.setExclusive(False)
        # self.SchemMapType.setChecked(True)
        self.MapType.buttonClicked.connect(self.updateLayer)

    def updateLayer(self):
        if self.MAP_IS_ACTIVE:
            self.getImage()

    def getImage(self):
        self.spn = list(map(lambda i: int(float(i) * 100), self.spn_pole.toPlainText().split(', ')))
        self.coords = list(map(float, self.coords_pole.toPlainText().split(', ')))

        # print(self.coords, self.spn)
        layer = {1: 'map', 2: 'sat', 3: 'skl'}
        map_request = (f"http://static-maps.yandex.ru/1.x/?ll={self.coords[1]},{self.coords[0]}"
                       f"&spn={self.spn[0] / 100},{self.spn[1] / 100}&l={layer[self.MapType.checkedId()]}")
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
        self.MAP_IS_ACTIVE = True
        self.spn_pole.setReadOnly(True)
        self.coords_pole.setReadOnly(True)

    def keyPressEvent(self, event) -> None:
        if event.key() == QtCore.Qt.Key_PageUp:
            if self.spn[0] < 15:
                self.spn[0] += 5
                self.spn[1] += 5
            else:
                self.spn[0] += 50
                self.spn[1] += 50
        elif event.key() == QtCore.Qt.Key_PageDown:
            if self.spn[0] < 50:
                self.spn[0] -= 5
                self.spn[1] -= 5
            elif self.spn[0] >= 50 and self.spn[1] >= 50:
                self.spn[0] -= 50
                self.spn[1] -= 50
        elif event.key() == QtCore.Qt.Key_D:
            self.coords[1] += self.spn[1] / 100
        elif event.key() == QtCore.Qt.Key_A:
            self.coords[1] -= self.spn[1] / 100
        elif event.key() == QtCore.Qt.Key_W:
            self.coords[0] += self.spn[0] / 100
        elif event.key() == QtCore.Qt.Key_S:
            self.coords[0] -= self.spn[0] / 100
        else:
            # print(event.key(), 'll')
            return None
        '''self.coords[0] = round(self.coords[0], 8)
        self.coords[1] = round(self.coords[1], 8)'''
        if self.spn[0] > 9000:
            self.spn[0] = 9000
        if self.spn[1] > 9000:
            self.spn[1] = 9000
        if self.spn[0] < 0:
            self.spn[0] = 0
        if self.spn[1] < 0:
            self.spn[1] = 0
        if self.coords[0] + self.spn[0] / 200 > 90:
            self.coords[0] = 90 - self.spn[0] / 200
        if self.coords[0] - self.spn[0] / 200 < -90:
            self.coords[0] = -90 + self.spn[0] / 200
        if self.coords[1] > 180:
            self.coords[1] = -180 + self.coords[1] + 180
        if self.coords[1] < -180:
            self.coords[1] = 180 + self.coords[1] + 180
        if self.coords[1] == 180:
            self.coords[1] = -180
        # print(self.coords, self.spn)
        self.coords_pole.setText(f'{self.coords[0]}, {self.coords[1]}')
        self.spn_pole.setText(f'{self.spn[0] / 100}, {self.spn[1] / 100}')
        #print(event.key)
        self.getImage()

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
