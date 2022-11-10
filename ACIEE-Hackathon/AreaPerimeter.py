import cv2
import numpy as np

class AreaPerimeter:

    def __init__(self):
        self.imgAdr = None

    def setImage(self, imageAdress):
        if type(imageAdress) is str:
            self.imgAdr = imageAdress
            return True
        else:
            return False

    def selectPerimArea(self):
        if self.imgAdr is None:
            return None

        img = cv2.imread(self.imgAdr)

        hg, wd, ch = img.shape
        minAmount = 800
        minArie = (hg * wd) / minAmount

        image = img.copy()
        # PROCESARE
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        # gray = cv2.GaussianBlur(gray, (11,11), 0)

        ret, thresh = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY_INV)

        # CONTURUL______________

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
        image_copy2 = img.copy()
        image = cv2.bitwise_and(image, image, mask=thresh)
        # CALCUL_________________
        ar = []
        max = -1
        for i, cnt in enumerate(contours):
            (x, y, w, h) = cv2.boundingRect(cnt)
            obj = cv2.resize(image[y:y + h, x:x + w, :], (w * 10, h * 10), interpolation=cv2.INTER_AREA)
            suma = np.mean(obj)
            ar.append([suma, cnt])
            if suma > max and (w * h) >= minArie:
                max = suma
                maxcnt = i

        # MINIM____________________

        image = cv2.bitwise_not(image)
        max = -1
        for i, cnt in enumerate(contours):
            (x, y, w, h) = cv2.boundingRect(cnt)
            obj = cv2.resize(image[y:y + h, x:x + w, :], (w * 10, h * 10), interpolation=cv2.INTER_AREA)
            suma = np.mean(obj)
            if suma > max and (w * h) >= minArie:
                max = suma
                minimcnt = i

        # ASCUNDERE____________________

        for i, cnt in enumerate(contours):
            if i == minimcnt or i == maxcnt:
                continue
            (x, y, w, h) = cv2.boundingRect(contours[i])
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), -1)

        # AFISARE_------------

        (x, y, w, h) = cv2.boundingRect(contours[maxcnt])
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        (x, y, w, h) = cv2.boundingRect(contours[minimcnt])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return img