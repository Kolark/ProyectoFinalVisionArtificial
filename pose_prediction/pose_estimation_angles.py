import cv2
import numpy as np

from maths.angles import AnglesFromRig
from maths.predictive_filter import PredictiveFilter

from pose_prediction import pose_types


class PoseEstimation:
    """
    Clase para calcular la pose
    """

    def __init__(self):
        """
        Constructor de la clase
        """

        MODE = "COCO"

        if MODE == "COCO":
            proto_file = "pose/coco/pose_deploy_linevec.prototxt"
            weights_file = "pose/coco/pose_iter_440000.caffemodel"
            self.n_points = 8

        elif MODE == "MPI":
            proto_file = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
            weights_file = "pose/mpi/pose_iter_160000.caffemodel"
            self.n_points = 8

        self.IN_WIDTH = 128
        self.IN_HEIGHT = 128
        self.THRESHOLD = 0.2

        self.net = cv2.dnn.readNetFromCaffe(proto_file, weights_file)

    def is_in_pose(self, frame, pose_type: int, rig=None):
        """
        Calcula si la pose es correcta

        :param frame: Frame de la cámara
        :param pose_type: tipo de pose a validar
        :param rig: si hay rig no lo vuelva a calcular
        :returns: Bool de si la pose es correcta o no
        """
        if rig:
            points = rig
        else:
            frame_width = frame.shape[1]
            frame_height = frame.shape[0]

            input_blob = cv2.dnn.blobFromImage(
                frame, 1.0 / 255, (self.IN_WIDTH, self.IN_HEIGHT), (0, 0, 0), swapRB=False, crop=False)
            self.net.setInput(input_blob)
            output = self.net.forward()
            H = output.shape[2]
            W = output.shape[3]

            points = []  # Empty list to store the detected keypoints

            for i in range(self.n_points):
                # confidence map of corresponding body's part.
                probMap = output[0, i, :, :]
                # Find global maxima of the probMap.
                _, prob, _, point = cv2.minMaxLoc(probMap)
                # Scale the point to fit on the original image
                x = int(frame_width * point[0] / W)
                # Scale the point to fit on the original image
                y = int(frame_height * point[1] / H)

                if prob > self.THRESHOLD:
                    points.append((x, y))
                else:
                    points.append(None)

        is_pose = False

        if pose_type == pose_types.ONE_ARM_UP:
            # Calcula si tiene la muñeca derecha más a la derecha y más arriba que el hombro
            try:
                # Calcula si está en la pose correcta
                is_pose = (points[7][0] > points[5][0] and
                           points[7][1] < points[5][1])
            except:
                is_pose = False
                points = None

            return is_pose, points

        elif pose_type == pose_types.TWO_ARMS_UP:
            # Calcula si tiene la muñeca derecha más a la derecha y más arriba que el hombro y lo mismo con la muñeca izquierda
            try:
                # Calcula si está en la pose correcta
                is_pose = (points[7][0] > points[5][0] and
                           points[7][1] < points[5][1] and
                           points[4][0] < points[2][0] and
                           points[4][1] < points[2][1])
            except:
                is_pose = False
                points = None

            return is_pose, None

        else:
            return False, None
