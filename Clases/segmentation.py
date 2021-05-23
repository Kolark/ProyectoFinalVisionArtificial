import cv2


class Segmentation:

    """Clase para realizar la segmentación con los valores otorgados por la calibración"""

    def __init__(self, HMin, SMin, VMin, HMax, SMax, VMax):
        """
        :param HMin: Minimum Hue
        :param VMin: Minimum Brightness
        :param SMin: Minimum Saturation
        :param HMax: Maximum Hue
        :param VMax: Maximum Brightness
        :param SMax: Maximum Saturation
        """

        # Crear el kernel para erosionar y dilatar
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

        self.HMin = HMin
        self.VMin = VMin
        self.SMin = SMin
        self.HMax = HMax
        self.VMax = VMax
        self.SMax = SMax

    def segmentate(self, originalImage):
        """
        Segmentates a image

        :param originalImage: The original image to segmentate
        :returns: The segmented image
        """

        # Convertir la imagen a hsv
        hsv = cv2.cvtColor(originalImage, cv2.COLOR_BGR2HSV)

        # Crear la máscara con los valores máximos y mínimos del hsv
        # Utilizando el hsv blurreado para mayor presición
        mask = cv2.inRange(hsv, (self.HMin, self.SMin, self.VMin),
                           (self.HMax, self.SMax, self.VMax))
        # Utilizar MORPH_OPEN (erosionar -> dilatar) utilizando el kernel
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)

        return mask
        """ # Crear imagen en bgr de hsv blurreado
        bgrblur = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        # Crear una imagen en escala de grises del frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Blurrear la imagen en escala de grises
        gray = cv2.blur(gray, (5, 5))
        # Crear una imagen de tres canales de la imagen en escala de grises blurreada
        bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
      
        # Separar el fondo del objeto clave
        background = cv2.bitwise_and(bgr, bgr, mask=255-mask)
        selected = cv2.bitwise_and(bgrblur, bgrblur, mask=mask)
        # selected = cv2.bitwise_and(frame, frame, mask=mask)
      
        # Juntar el fondo en escala de grises y el objeto a color
        output = cv2.add(background, selected) """
