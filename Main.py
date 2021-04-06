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

wall4=Wall(100,150,200,230,scene)
#wall5=Wall(200,350,150,250,scene)

wall6=Wall(260,150,300,250,scene)

door=Door(400,100,scene)

walls=[wall1,wall2,wall3,wall4,wall6]

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
model.Simulate(0.1)
model.FilterKalman(0.1)
graphicsView.show()


import matplotlib.pyplot as plt

t=[]
a=[]
for j in model.RealData:
    t.append(j[0])
    a.append(j[3])

ai=[]
for j in model.Y:
    ai.append(j[2][2])

afk=[]
for j in model.Result:
    afk.append(j[3])

plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("График Курса") # заголовок
plt.xlabel("t, сек.") # ось абсцисс
plt.ylabel("angle, мм.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, a,'r',label="Реальное значение Курса")  # построение графика
plt.plot(t, afk,'b',label="Результат Курса - ФК")  # построение графика
plt.plot(t, ai,'g',label="Результат измерения Курса - ФК")  # построение графика
plt.legend(loc=0)
plt.savefig('Эволюция компоненты Курса')


t=[]
x=[]
y=[]
rx=[]
ry=[]
for j in model.RealData:
    t.append(j[0])
    x.append(j[1])
    y.append(j[2])
    rx.append(j[4])
    ry.append(j[5])

xi=[]
yi=[]
rxi=[]
for j in model.Y:
    xi.append(j[2][0])
    yi.append(j[2][1])
    #rxi.append(j[3][3])

xfk=[]
yfk=[]
rxfk=[]
ryfk=[]
for j in model.Result:
    xfk.append(j[1])
    yfk.append(j[2])
    rxfk.append(j[4])
    ryfk.append(j[5])

p_x=[]
p_y=[]
p_a=[]
p_rx=[]
p_ry=[]
for p in model.P:
    p_x.append(p[1])
    p_y.append(p[2])
    p_a.append(p[3])
    p_rx.append(p[4])   
    p_ry.append(p[5])    

plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("График эволюции по Y") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("y, см.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, ry,'r',label="Реальное значение траектории")  # построение графика
plt.plot(t, ryfk,'b',label="Результат - ФК")  # построение графика
#plt.plot(t, yi,'g',label="Результат измерения- ФК")  # построение графика
plt.legend(loc=0)
plt.savefig('Траектория движения Y')

plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("График эволюции по X") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("x, см.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, rx,'r',label="Реальное значение траектории")  # построение графика
plt.plot(t, rxfk,'b',label="Результат - ФК")  # построение графика
plt.plot(t, x,'g',label="БИНС")  # построение графика
#plt.plot(t, xi,'g',label="Результат измерения- ФК")  # построение графика
plt.legend(loc=0)
plt.savefig('Траектория движения X')



plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("Корелляционная трубка X") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("x, см.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, np.asarray(x)-np.asarray(xfk),'r',label="Ошибка")  # построение графика
plt.plot(t, np.sqrt(p_x)*3,'b',label="Трубка сверху")  # построение графика
plt.plot(t, -np.sqrt(np.asarray(p_x))*3,'b',label="Трубка снизу")  # построение графика
plt.legend(loc=0)
plt.savefig('Корелляционная трубка X')

plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("Корелляционная трубка Y") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("y, см.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, np.asarray(y)-np.asarray(yfk),'r',label="Ошибка")  # построение графика
plt.plot(t, np.sqrt(p_y)*3,'b',label="Трубка сверху")  # построение графика
plt.plot(t, -np.sqrt(np.asarray(p_y))*3,'b',label="Трубка снизу")  # построение графика
plt.legend(loc=0)
plt.savefig('Корелляционная трубка Y')


plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("Корелляционная трубка Alpha") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("alpha, градусов.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, np.asarray(a)-np.asarray(afk),'r',label="Ошибка")  # построение графика
plt.plot(t, np.sqrt(p_a)*3,'b',label="Трубка сверху")  # построение графика
plt.plot(t, -np.sqrt(np.asarray(p_a))*3,'b',label="Трубка снизу")  # построение графика
plt.legend(loc=0)
plt.savefig('Корелляционная трубка Alpha')


plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("Корелляционная трубка положения робота X") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("x, см.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, np.asarray(rx)-np.asarray(rxfk),'r',label="Ошибка")  # построение графика
plt.plot(t, np.sqrt(p_rx)*3,'b',label="Трубка сверху")  # построение графика
plt.plot(t, -np.sqrt(np.asarray(p_rx))*3,'b',label="Трубка снизу")  # построение графика
plt.legend(loc=0)
plt.savefig('Корелляционная трубка положения робота X')

plt.figure(figsize=(24,12))
plt.rc('axes', labelsize=30)
plt.rc('axes',titlesize=30)
plt.rc('legend', fontsize=30)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.title("Корелляционная трубка положения робота Y") # заголовок
plt.xlabel("t, с.") # ось абсцисс
plt.ylabel("x, см.") # ось ординат
plt.grid()      # включение отображение сетки
plt.plot(t, np.asarray(ry)-np.asarray(ryfk),'r',label="Ошибка")  # построение графика
plt.plot(t, np.sqrt(p_ry)*3,'b',label="Трубка сверху")  # построение графика
plt.plot(t, -np.sqrt(np.asarray(p_ry))*3,'b',label="Трубка снизу")  # построение графика
plt.legend(loc=0)
plt.savefig('Корелляционная трубка положения робота Y')

sys.exit(app.exec())