import cv2
import numpy as np

def mapRange(num, in_min, in_max, out_min, out_max):
    return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class SymmetryDetector:

    def __init__(self):
        self.imgAdr = None

    def setImage(self, imageAdress):
        if type(imageAdress) is str:
            self.imgAdr = imageAdress
            return True
        else:
            return False

    def removeSymetricItems(self, percentageThreshold):
        if self.imgAdr is None:
            return None

        image = cv2.imread(self.imgAdr)
        img = image.copy()
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img_gray1 = cv2.blur(img_gray, (5, 5))

        _, thresh = cv2.threshold(img_gray1, 235, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)

        image_copy2 = img.copy()
        cv2.drawContours(image_copy2, contours, -1, (0, 255, 0), 2, cv2.LINE_AA)

        for i, cnt in enumerate(contours):
            (x, y, w, h) = cv2.boundingRect(cnt)

            obj = thresh[y:y + h, x:x + w]

            pObj = cv2.arcLength(cnt, True)

            maxper = 0
            deltap = 0

            for ang in range(60):
                M = cv2.getRotationMatrix2D((w / 2, h / 2), ang * 3, 0.75)
                objrot = cv2.warpAffine(obj, M, (w, h))
                objrotflip = cv2.flip(objrot, 1)

                bitwiseAnd = cv2.bitwise_and(objrot, objrotflip)

                contBit, _ = cv2.findContours(bitwiseAnd, cv2.RETR_EXTERNAL,
                                              cv2.CHAIN_APPROX_SIMPLE)

                pObjBit = cv2.arcLength(contBit[0], True)

                perObj = mapRange(np.sum(bitwiseAnd) / np.sum(objrot) * 100, 40, 100, 0, 100)

                deltap = (pObj - pObjBit) / pObj * 100

                finalPer = perObj * 0.8 + 0.2 * deltap

                if maxper < finalPer:
                    maxper = finalPer

            maxper = round(maxper, 2)
            print(str(i + 1) + "  " + str(maxper) + "%")

            if maxper > percentageThreshold:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), -1)

        return img