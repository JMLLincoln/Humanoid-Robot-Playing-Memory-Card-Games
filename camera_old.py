import cv2
import numpy as np

from skimage.measure import compare_ssim as ssim

class camera:

    def __init__(self, run):
        
        self.cap = cv2.VideoCapture(0)
        
        self.image = None
        self.gray = None
        self.binary = None

        self.cards = {}
        self.c_id = 65
        
        self.box_points = []
        self.card_bin = []

        self.done = False

        if run:
            self.loop()

    def loop(self):
        run = True
        while(run):
            self.store_frame()
            self.morph_proc_main()
            self.detect_objects()
            self.proc_cards()
            self.out(image = True, binary = True)

            if self.card_bin and not self.done:
                print("\nCOMPARE")
                for i in range(1, len(self.card_bin)):
                    for j in range(i+1, len(self.card_bin)+1):
                        print("%s by %s:" % (i, j))
                        t = self.compare_images(self.card_bin[i-1], self.card_bin[j-1])
                        if t:
                            print("\n\nSuccessful match with: %s and %s" % (i, j))

                self.done = True

            self.c_id = 65
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                run = False

        self.quit()
        
    def store_frame(self):
        
        ret1, self.image = self.cap.read()
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Playing Cards
        #ret2, self.binary = cv2.threshold(self.gray, 150, 255,
        #                                  cv2.THRESH_BINARY)
        
        # Handmade Cards
        ret2, self.binary = cv2.threshold(self.gray, 100, 255,
                                          cv2.THRESH_BINARY)
    
    def out(self, image = False, gray = False, binary = False):

        if image:
            cv2.imshow('colour', self.image)

        if gray:
            cv2.imshow('gray', self.gray)

        if binary:
            cv2.imshow('binary', self.binary)

        i = 0
        for b in self.card_bin:
            i += 1
            try:
                cv2.imshow(str(i), b)
            except:
                pass

    def quit(self):
        
        self.cap.release()
        cv2.destroyAllWindows()

    def morph_proc_main(self):

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        self.binary = cv2.morphologyEx(self.binary, cv2.MORPH_CLOSE, kernel)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        self.binary = cv2.erode(self.binary, kernel, iterations = 3)
        self.binary = cv2.dilate(self.binary, kernel, iterations = 3)
        
    def detect_objects(self):

        im, contours, hierarchy = cv2.findContours(self.binary, cv2.RETR_TREE,
                                                    cv2.CHAIN_APPROX_SIMPLE)

        try:
            self.find_cards(contours, hierarchy[0])
        except Exception as e:
            print("Waiting for image feed...")

        self.box_points = []
        for k, v in self.cards.items():
            for con in v:
                self.box_points.append(self.create_box(con))
                
        self.draw_contours()

    def create_box(self, con):
        
        rect = cv2.minAreaRect(con)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        return box

    def draw_contours(self):

        for box in self.box_points:
            cv2.drawContours(self.image, [box], -1, (0, 255, 0), 2)

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

            # Playing Cards: 30000
            # Handmade Cards: 14000
            if area > 14000:
                key = self.get_id()
                value = [cons[i]]
                #for k in kids:
                #    value.append(cons[k])

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

    def proc_cards(self):

        self.card_bin = []
        i = -1
        for box in self.box_points:
            i += 1
            
            self.card_bin.append(self.rotate_card(box))
            self.card_bin[i] = self.card_bin[i][25:134, 25:113]
            self.card_bin[i] = 255 - self.card_bin[i]
            
    def rotate_card(self, box):
        
        pts_dst = np.array([[138.0, 159.0],
                            [0.0, 159.0],
                            [0.0, 0.0],
                            [138.0, 0.0]])

        im_dst = np.zeros((159, 138, 3), np.uint8)
        h, status = cv2.findHomography(box, pts_dst)

        return cv2.warpPerspective(self.binary, h, (im_dst.shape[1], im_dst.shape[0]))

    def compare_images(self, A, B):
        
        err = np.sum((A.astype("float") - B.astype("float")) ** 2)
        err /= float(A.shape[0] * A.shape[1])

        print("M: %s" % err)

        ssim_none = ssim(A, B, data_range = A.max() - A.min())

        print("S: %s" % ssim_none)

        im, c1, hierarchy = cv2.findContours(A, 1, 2)
        p1 = cv2.arcLength(c1[0], True)
        
        im, c2, hierarchy = cv2.findContours(B, 1, 2)
        p2 = cv2.arcLength(c2[0], True)

        if p1 > p2:
            p = p1 - p2
        else:
            p = p2 - p1
            
        print("P: %s" % p)

        if err > 5000 or ssim_none < 0.75 or p > 20:
            return False
        else:
            return True
            

c = camera(run = True)






