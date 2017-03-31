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
        img = cv2.medianBlur(img,5)

        ret,th1 = cv2.threshold(img,40,255,cv2.THRESH_BINARY)
        th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                    cv2.THRESH_BINARY,11,2)
        th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv2.THRESH_BINARY,11,2)

        titles = ['Original Image', 'Global Thresholding (v = 127)',
                    'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
        images = [img, th1, th2, th3]

        for i in xrange(4):
            plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
            plt.title(titles[i])
            plt.xticks([]),plt.yticks([])
        plt.show()
        break
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
