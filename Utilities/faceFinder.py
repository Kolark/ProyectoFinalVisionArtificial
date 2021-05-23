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
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 4)
        if len(faces) > 0:
            return faces[0], True
        else:
            h, w = gray.shape
            return (w//2, h//2, 0, 0), False