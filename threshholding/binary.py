import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('colour',frame)
    cv2.imshow('gray', gray)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        cv2.imwrite('col.png', frame)
        img = cv2.imread('col.png',0)
        ret,thresh1 = cv2.threshold(img,40,255,cv2.THRESH_BINARY)
        ret,thresh2 = cv2.threshold(img,40,255,cv2.THRESH_BINARY_INV)

        titles = ['Original Image','BINARY','BINARY_INV']
        images = [img, thresh1, thresh2]

        for i in xrange(3):
            plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
            plt.title(titles[i])
            plt.xticks([]),plt.yticks([])

        plt.show()
        break
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
