import cv2

class BrightnessSelector:

    def __init__(self):
        self.imgAdr = None

    def setImage(self, imageAdress):
        if type(imageAdress) is str:
            self.imgAdr = imageAdress
            return True
        else:
            return False

    def checkBrightness(self):
        if self.imgAdr is None:
            return None

        #IMAGINEA________________
        img = cv2.imread(self.imgAdr)
        image = img.copy()
        #PROCESARE
        img_gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        hg, wd, ch = img.shape
        minAmount = 800
        minArie = (hg* wd)/minAmount

        #img_gray1 = cv2.GaussianBlur(img_gray1, (11,11), 0)

        ret, thresh1 = cv2.threshold(img_gray1, 230, 255, cv2.THRESH_BINARY_INV)

        #CONTURUL______________

        contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_EXTERNAL,
                                                 cv2.CHAIN_APPROX_SIMPLE)
        image_copy2 = img.copy()

        #ARIA _________________
        max = 0
        for i,cnt in enumerate(contours):
            (x,y,w,h) = cv2.boundingRect(cnt)
            var = cv2.contourArea(cnt)
            if var > max and (w*h) >= minArie:
                maxCnt = i
                max = var

        #PERIMETRUL ___________

        min = (hg+wd)*2
        for i,cnt in enumerate(contours):
            (x,y,w,h) = cv2.boundingRect(cnt)
            var = cv2.arcLength(cnt,True)
            if var < min and (w*h) >= minArie:
                minCnt = i
                min = var

        #ASCUNDERE_________________________

        for i,cnt in enumerate(contours):
            if i == minCnt or i == maxCnt:
                continue
            (x,y,w,h) = cv2.boundingRect(contours[i])
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255),-1)

        #AFISARE ________________
        (x,y,w,h) = cv2.boundingRect(contours[maxCnt])
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0),2)
        (x,y,w,h) = cv2.boundingRect(contours[minCnt])
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255),2)

        return img