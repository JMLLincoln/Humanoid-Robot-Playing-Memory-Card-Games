import cv2
import numpy as np

class camera:

    def __init__(self, run):
        
        self.cap = cv2.VideoCapture(0)
        
        self.image = None
        self.gray = None
        self.binary = None

        self.cards = {}
        self.c_id = 65
        
        if run:
            self.loop()        

    def loop(self):
        
        run = True
        while(run):
            self.store_frame()
            self.morph_proc()
            self.detect_objects()
            self.out(image = True, binary = True)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                run = False   

        self.quit()
        
    def store_frame(self):
        
        ret1, self.image = self.cap.read()
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        ret2, self.binary = cv2.threshold(self.gray, 150, 255,
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

    def morph_proc(self):

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        self.binary = cv2.morphologyEx(self.binary, cv2.MORPH_CLOSE, kernel)
        
    def detect_objects(self):

        im, contours, hierarchy = cv2.findContours(self.binary, cv2.RETR_TREE,
                                                    cv2.CHAIN_APPROX_SIMPLE)

        try:
            self.find_cards(contours, hierarchy[0])
        except Exception as e:
            print("Waiting for image feed...")
            print(e)

        for card in self.cards.items():
            for con in card[1]:
                self.draw_contour(con)
            

    def draw_contour(self, con):
        rect = cv2.minAreaRect(con)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        cv2.drawContours(self.image, [box], -1, (0,255,0), 3)

    def find_cards(self, cons, data):
        
        self.cards = {}
        """
        {ID: [own contour, [child contours]]}
        """
        for i in range(len(cons)):

            x = data[i][2]
            if x > -1:
                kids = self.recur_children(data, x)
            else:
                continue
                
            if len(kids) > 0 and len(kids) < 5:
                area = cv2.contourArea(cons[i])
            else:
                area = 0 
            
            if area > 30000:
                key = self.get_id()
                value = [cons[i]]
                for k in kids:
                    value.append(cons[k])

                self.cards[key] = value

    def recur_children(self, d, x):
        
        if x == -1:
            return []
        else:
            x = d[x][0]
            return [x] + self.recur_children(d, x)

    def get_id(self):
        x = chr(self.c_id)
        self.c_id += 1
        return x
        
c = camera(run = True)






