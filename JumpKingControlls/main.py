import cv2
import numpy as np

from clases.tools import Characteristics


LEFT = 0
RIGHT = 1

WIDTH = HEIGHT = 0

LEFT_PORCENT = RIGHT_PORCENT = 40
BOTTON_PORCENT = 35


last_side = None


camera = cv2.VideoCapture(0)

# Start
available, frame = camera.read()

if available:
    HEIGHT, WIDTH, _ = frame.shape


# Update
while True:
    available, frame = camera.read()

    if not available:
        print("Cámara no disponible")
        break

    frame = cv2.flip(frame, 1)

    # Límite izquierdo

    # Convertirlo a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    dimensiones, face_found = Characteristics.find_face(gray)
    
    # Si no encontró un rostro
    if face_found:
        print(dimensiones)
        cv2.rectangle(gray, (dimensiones[0], dimensiones[1]), (dimensiones[0] + dimensiones[2], dimensiones[1] + dimensiones[3]), (255, 255, 255), 2)
    # Si encontró un rostro

    cv2.imshow("Camera", gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()

cv2.destroyAllWindows()
