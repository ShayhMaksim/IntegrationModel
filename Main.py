from Door import Door
from Wall import Wall
from Room import Room
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

graphicsView.show()

sys.exit(app.exec())