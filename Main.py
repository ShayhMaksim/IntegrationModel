from typing import List
from Model import Model
from Door import Door
from Wall import Wall
from Room import Room
from QrCode import QrCode
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

room=Room(0,0,400,scene)

wall1=Wall(100,200,200,300,scene)
wall2=Wall(100,150,300,100,scene)
wall3=Wall(300,150,250,300,scene)

door=Door(400,100,scene)

walls=[wall1,wall2,wall3]

QrCode1=QrCode(0,50,-np.pi*3./2.,scene)
QrCode2=QrCode(50,0,-0,scene)

QrCode3=QrCode(50,400,-np.pi,scene)
QrCode4=QrCode(0,400-50,-np.pi*3./2.,scene)

QrCode5=QrCode(400,50,-np.pi*0.5,scene)
QrCode6=QrCode(400-50,0,-0,scene)

QrCode7=QrCode(400,400-50,-np.pi*0.5,scene)
QrCode8=QrCode(400-50,400,-np.pi,scene)

qrList=[QrCode1,QrCode2,QrCode3,QrCode4,QrCode5,QrCode6,QrCode7,QrCode8]
model=Model(50,300,scene,room,door,walls)
model.AddQrCode(qrList)
model.Simulate(0.25)

graphicsView.show()

sys.exit(app.exec())