import cv2
import math

def hconcat_resize(img_list,
                   interpolation
                   =cv2.INTER_CUBIC):
    # take minimum hights
    h_max = max(img.shape[0]
                for img in img_list)

    # image resizing
    im_list_resize = [cv2.copyMakeBorder(img, int(math.floor(h_max-img.shape[0]/2)), int(math.ceil(h_max-img.shape[0]/2)), 3, 3, borderType=cv2.BORDER_CONSTANT, value=(255,255,255,0))
                      for img in img_list]

    # return final image
    return cv2.hconcat(im_list_resize)

class ObjectSort:

    def __init__(self):
        self.imgAdr = None

    def setImage(self, imageAdress):
        if type(imageAdress) is str:
            self.imgAdr = imageAdress
            return True
        else:
            return False

    def sortByArea(self):
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

        obj = []

        contours = sorted(contours, key=lambda c: cv2.contourArea(c), reverse=True)
        for i, cnt in enumerate(contours):
            (x, y, w, h) = cv2.boundingRect(cnt)

            ob = image[y:y + h, x:x + w,:]

            obj.append(ob)

        img = hconcat_resize(obj)
        return img