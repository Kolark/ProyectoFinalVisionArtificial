#Import libraries
import sys,re
#region PYQT5 libraries
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
#endregion

import numpy as np
import cv2
from Utilities.faceFinder import Characteristics

from Utilities.timeManager import TimeManager
#region UI and initial Camera Capture
#.ui file path
uiFile = "./ui/finalUI.ui"
#Load ui file
Ui_MainWindow, QtBaseClass = uic.loadUiType(uiFile)
#Capture video
captura = cv2.VideoCapture(0)

#endregion




class UIWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        #region initial Setup
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)
        self.controlTimer()
        self.estado = 0

        self.faceOFFtimeManager = TimeManager()
        self.faceOFFtimeManager.startTimer()
        self.faceONtimeManager = TimeManager()
        self.faceONtimeManager.startTimer()
        #endregion
    
    def viewCam(self):
    # read imageS in BGR format
        disponible, fotograma = captura.read()
        fotograma = cv2.flip(fotograma,1)
        # fotograma = Clases.tools.Quality.makebetter(fotograma)
        h, w, channel = fotograma.shape    
        # convert image to RGB format
        #region MAQUINA DE ESTADOS
        dimensiones, face_found = Characteristics.find_face(fotograma)
        if face_found:
            cv2.rectangle(fotograma, (dimensiones[0], dimensiones[1]), (dimensiones[0] + dimensiones[2], dimensiones[1] + dimensiones[3]), (255, 255, 255), 2)
            self.faceOFFtimeManager.RestartTimer()
        else:
            self.faceONtimeManager.RestartTimer()

        if(self.estado == 0):
            print("VEN A JUGAR")
            if(face_found):
                self.estado = 1 
        elif(self.estado == 1):
            print("VAS A JUGAR EN " + str(5 - self.faceONtimeManager.getTimePassed()))
            if(not face_found):
                self.estado = 0
            elif(self.faceONtimeManager.getTimePassed() > 5):
                self.estado = 3
        elif(self.estado == 3):
            print("JUGANDO")

        elif(self.estado == 4):
            print("Gracias por jugar")
                



        
        
        #endregion



    #Set image to QLabel
        fotogramaRGB = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
        self.SetImages(fotogramaRGB,self.cameraLabel)
        self.timeLabel.setText(str(np.round(self.faceOFFtimeManager.getTimePassed())))
        


    def SetImages(self,IMG,label):
        h, w, channel = IMG.shape        
        step = channel * w
        
        qImg = QImage(IMG.data, w, h, step, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qImg))
        

        

    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(16)
            # update control_bt text
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text

if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = UIWindow()
    window.show()
    sys.exit(app.exec_())

    