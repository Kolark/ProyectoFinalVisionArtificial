# Import libraries
import sys
import re
# region PYQT5 libraries
from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
# endregion

import numpy as np
import cv2
from Utilities.faceFinder import Characteristics

from Utilities.timeManager import TimeManager

from pose_prediction.pose_estimation_angles import PoseEstimation
from pose_prediction import pose_types
from Utilities.UDPsend import SendToUnity
# region UI and initial Camera Capture
# .ui file path
uiFile = "./ui/finalUI.ui"
# Load ui file
Ui_MainWindow, QtBaseClass = uic.loadUiType(uiFile)
# Capture video
captura = cv2.VideoCapture(0)

# endregion


class UIWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        # region initial Setup
        self.setupUi(self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)
        self.controlTimer()
        self.estado = 0

        self.faceOFFtimeManager = TimeManager()
        self.faceOFFtimeManager.startTimer()
        self.faceONtimeManager = TimeManager()
        self.faceONtimeManager.startTimer()

        self.leftPos = 210
        self.rightPos = 210

        self.InvitationBool = False
        self.LoadingBool = False
        self.LeftBool = False
        self.CenterBoolNOPOSE = False
        self.CenterBoolONEARM = False
        self.CenterBoolTWOARM = False
        self.RightBool = False

        # Pose
        self.pose_estimation = PoseEstimation()

        self.is_pose1Arm = False
        self.is_pose2Arms = False

        self.rig = None

        # endregion

    def viewCam(self):
        # read imageS in BGR format
        disponible, fotograma = captura.read()
        fotograma = cv2.flip(fotograma, 1)
        # fotograma = Clases.tools.Quality.makebetter(fotograma)
        h, w, channel = fotograma.shape
        # convert image to RGB format
        # region MAQUINA DE ESTADOS
        dimensiones, face_found = Characteristics.find_face(fotograma)

        if face_found:
            cv2.rectangle(fotograma, (dimensiones[0], dimensiones[1]), (
                dimensiones[0] + dimensiones[2], dimensiones[1] + dimensiones[3]), (255, 255, 255), 2)
            cv2.circle(fotograma, (dimensiones[0] + dimensiones[2]//2,
                                   dimensiones[1] + dimensiones[3]//2), 25, (0, 255, 0), 1)
            self.faceOFFtimeManager.RestartTimer()
        else:
            self.faceONtimeManager.RestartTimer()

        if(self.estado == 0):
            print("VEN A JUGAR")
            self.setBooleans(True, False, False, False, False, False, False)
            if(face_found):
                self.estado = 1
        elif(self.estado == 1):
            print("VAS A JUGAR EN " +
                  str(5 - self.faceONtimeManager.getTimePassed()))
            self.setBooleans(False, True, False, False, False, False, False)
            if(not face_found):
                self.estado = 0
            elif(self.faceONtimeManager.getTimePassed() > 5):
                self.estado = 3
        elif(self.estado == 3):

            cv2.rectangle(fotograma, (0, 0), (self.leftPos, h), (0, 255, 0), 5)
            cv2.rectangle(fotograma, (w-self.rightPos, 0),
                          (w, h), (255, 0, 0), 5)
            posX = dimensiones[0] + dimensiones[2]//2
            if(face_found):
                if(posX < self.leftPos):
                    # SendToUnity('RIGHT')
                    self.setBooleans(False, False, True,
                                     False, False, False, False)
                    print("IZQUIERDA")
                elif(posX < w-self.rightPos):

                    is_one_arm_pose, self.rig = self.pose_estimation.is_in_pose(
                        fotograma, pose_types.ONE_ARM_UP, self.rig)

                    if is_one_arm_pose:
                        is_two_arms_pose, self.rig = self.pose_estimation.is_in_pose(
                            fotograma, pose_types.TWO_ARMS_UP, self.rig)
                        if is_two_arms_pose:
                            print("Shoot")
                            self.setBooleans(
                                False, False, False, False, False, True, False)
                        else:
                            print("Charge")
                            self.setBooleans(
                                False, False, False, False, True, False, False)
                    else:
                        self.rig = None
                        self.setBooleans(False, False, False,
                                         True, False, False, False)
                        # SendToUnity('CENTER')
                        print("No pose")

                    # self.setBooleans(False, False, False, True, False)
                    # print("CENTRO")
                else:
                    self.setBooleans(False, False, False,
                                     False, False, False, True)
                    # SendToUnity('LEFT')
                    print("DERECHA")
            elif(int(np.round(self.faceOFFtimeManager.getTimePassed())) > 10):
                self.estado = 0
        # elif(self.estado == 4):
        #     print("Gracias por jugar")

        # endregion

    # Set image to QLabel
        fotogramaRGB = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
        self.SetImages(fotogramaRGB, self.cameraLabel)
        self.timeLabel.setText(
            str(np.round(self.faceOFFtimeManager.getTimePassed())))

    def setBooleans(self, inv, load, left, centernopose, centeronearm, centertwoarm, right):

        if(inv is True and self.InvitationBool is False):
            print("Change to INV")
            SendToUnity('INV')
        if(load is True and self.LoadingBool is False):
            print("Change to LOAD")
            SendToUnity('LOAD')
        if(left is True and self.LeftBool is False):
            SendToUnity('RIGHT')
            print("Change to LEFT")

        if(centernopose is True and self.CenterBoolNOPOSE is False):
            print("Change to CENTERNOPOSE")
            SendToUnity('CENTER')
        if(centeronearm is True and self.CenterBoolONEARM is False):
            print("Change to CENTERONEARM")
            SendToUnity('CENTER1')
        if(centertwoarm is True and self.CenterBoolTWOARM is False):
            print("Change to CENTERTWOARM")
            SendToUnity('SHOOT')

        if(right is True and self.RightBool is False):
            SendToUnity('LEFT')
            print("Change to RIGHT")

        self.InvitationBool = inv
        self.LoadingBool = load
        self.LeftBool = left
        self.CenterBoolNOPOSE = centernopose
        self.CenterBoolONEARM = centeronearm
        self.CenterBoolTWOARM = centertwoarm
        self.RightBool = right

    def SetImages(self, IMG, label):
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
    app = QtWidgets.QApplication(sys.argv)
    window = UIWindow()
    window.show()
    sys.exit(app.exec_())
