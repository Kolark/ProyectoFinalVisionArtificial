import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


class Characteristics:
    """Clase para detectar características"""

    @staticmethod
    def find_face(frame):
        """
        Método para encontrar un rostro en una imagen

        :param frame: imagen en donde están los rostros
        :returns: posición en x, y, ancho, alto y si encontró rostro
        """

        faces = face_cascade.detectMultiScale(frame, 1.3, 4)
        if len(faces) > 0:
            print("FOUND")
            return faces[0], True
        else:
            h, w = frame.shape
            print("NOT FOUND")
            return (w//2, h//2, 0, 0), False
