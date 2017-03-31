import cv2
import numpy as np

class camera:

    def __init__(self, run):
        
        self.cap = cv2.VideoCapture(0)
        
        self.image = None
        self.gray = None
        self.binary = None

        if run:
            self.loop()

    def loop(self):
        
        run = True
        while(run):
            self.store_frame()
            self.out(image = True, binary = True)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                run = False   

        self.quit()
        
    def store_frame(self):
        
        ret1, self.image = self.cap.read()
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        ret2, self.binary = cv2.threshold(self.gray, 110, 255,
                                          cv2.THRESH_BINARY)
    
    def out(self, image = False, gray = False, binary = False):

        if image:
            cv2.imshow('colour', self.image)

        if gray:
            cv2.imshow('gray', self.gray)

        if binary:
            cv2.imshow('binary', self.binary)

    def quit(self):
        
        self.cap.release()
        cv2.destroyAllWindows()
        
c = camera(run = True)






