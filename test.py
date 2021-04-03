from PyQt5.QtGui import QPen
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QWidget,QApplication,QGraphicsView,QGraphicsScene
from PyQt5.QtGui import QPainter, QColor, QPen,QBrush
from PyQt5.QtCore import QRectF
import sys

app = QApplication(sys.argv)
scene = QGraphicsScene()
graphicsView = QGraphicsView(scene)
graphicsView.setWindowTitle("Комплексирование информационных приборов")
graphicsView.show()
graphicsView.resize(800,600)
#границы комнаты
scene.addLine(0,0,0,400)
scene.addLine(0,0,400,0)
scene.addLine(400,0,400,400)
scene.addLine(0,400,400,400)
#стартовая точка
scene.addEllipse(20,300,20,20,QPen(QColor(100,100,100)),QBrush(QColor(255,50,50)))
#барьеры
scene.addLine(100,200,200,300,QPen(QColor(100,255,100)))
scene.addLine(100,150,300,100,QPen(QColor(100,255,100)))
scene.addLine(300,150,250,300,QPen(QColor(100,255,100)))
#scene.addEllipse(400,0,30,30)
#выход
scene.addRect(QRectF(400,100,20,40),QColor(0,0,255))
#QR-коды
scene.addEllipse(-10,50,20,20)
scene.addEllipse(50,-10,20,20)

scene.addEllipse(50,400-10,20,20)
scene.addEllipse(400-10,50,20,20)

scene.addEllipse(400-10-50,-10,20,20)
scene.addEllipse(-10,400-10-50,20,20)

scene.addEllipse(400-10,400-10-50,20,20)
scene.addEllipse(400-10-50,400-10,20,20)

sys.exit(app.exec())