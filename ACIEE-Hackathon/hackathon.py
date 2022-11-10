import cv2
import numpy as np
import matplotlib.pyplot as plt
from SymmetryDetector import SymmetryDetector
from AreaPerimeter import AreaPerimeter
from Brightness import BrightnessSelector
from ObjectSort import ObjectSort

def toRGB(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

class Solver:

    def __init__(self):
        self.imgAdr = None

    def setImage(self, imageAdress):
        if type(imageAdress) is str:
            self.imgAdr = imageAdress
            return True
        else:
            return False

    def solve(self):
        if self.imgAdr is None:
            return None

        symdet = SymmetryDetector()
        symdet.setImage(self.imgAdr)

        apdet = AreaPerimeter()
        apdet.setImage(self.imgAdr)

        brgdet = BrightnessSelector()
        brgdet.setImage(self.imgAdr)

        obsort = ObjectSort()
        obsort.setImage(self.imgAdr)

        original = cv2.imread(self.imgAdr)

        fig = plt.figure(figsize=(10,10))

        fig.add_subplot(2,2,1)
        plt.imshow(toRGB(obsort.sortByArea()))
        plt.title("Object sort by size")

        fig.add_subplot(2, 2, 2)
        plt.imshow(toRGB(apdet.selectPerimArea()))
        plt.title("Largest area and smallest perim")

        fig.add_subplot(2, 2, 3)
        plt.imshow(toRGB(brgdet.checkBrightness()))
        plt.title("Brightest and darkest objects")

        fig.add_subplot(2,2,4)
        plt.imshow(toRGB(symdet.removeSymetricItems(80)))
        plt.title("Symmetric objects removed")

        plt.show()

test = Solver()

test.setImage('image.png')

test.solve()