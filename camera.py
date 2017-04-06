import cv2
import math
import numpy as np

class Feed:
    ''' Handles the camera feed and returns:
            BGR Images,
            Grayscale Images,
            Binary Images,
            Morphological Processing,
            Contours,
            Hierarchy,
            Image Comparisons

        Make sure to always run 'feed.end_cycle()' at
        the end of the main loop that involves this
        class.

        This makes sure the output has time to
        update and gives the user a way to close all 
        currently open windows '''
    
    def __init__(self):
        ''' Initialise the camera feed '''
        self.cap = cv2.VideoCapture(0)
        
    def store_frame(self):
        ''' Return the current frame of the camera feed '''
        ret, fr = self.cap.read()
        return fr

    def to_gray(self, colour):
        ''' Take an RGB image and return a grayscale image '''
        gr = cv2.cvtColor(colour, cv2.COLOR_BGR2GRAY)
        return gr

    def to_binary(self, gray, lower, upper):
        ''' Take a grayscale image and return a binary image based
            on upper and lower bounds '''
        ret, bi = cv2.threshold(gray, lower, upper, cv2.THRESH_BINARY)
        return bi
    
    def open(self, size, binary):
        ''' Morphologically open a binary image '''
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, size)
        return cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    def close(self, size, binary):
        ''' Morphologically close a binary image '''
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, size)
        return cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    def erode(self, size, binary, n):
        ''' Morphologically erode a binary image n times '''
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, size)
        return cv2.erode(binary, kernel, iterations = n)

    def dilate(self, size, binary, n):
        ''' Morphologically dilate a binary image n times '''
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, size)
        return cv2.dilate(binary, kernel, iterations = n)

    def get_contours(self, binary):
        ''' Take a binary image and return the contours and hierarchy '''
        im, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE,
                                                   cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierarchy

    def remove_contours(self, contours, lower, upper):
        ''' Return a list of contours with an area in between the
            lower and upper limits '''
        new_cons = []
        for con in contours:
            area = cv2.contourArea(con)
            if area > lower and area < upper:
                new_cons.append(con)
        return new_cons

    def create_rect(self, contour):
        ''' Take a contour and return a rectangle as a list
            so it's compatible with cv2.drawContours '''
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = [np.int0(box)]
        return box
    
    def rotate_image(self, image, center, theta, height, width):
        ''' Change the rotation of an image by theta degrees
            around the center point '''
        center = (height / 2, width / 2)
        M = cv2.getRotationMatrix2D(center, theta, 1)
        output = cv2.warpAffine(image, M, (height, width))
        return output

    def count_values(self, binary):
        ''' Takes an image and counts the 0 and >0 values '''
        white = cv2.countNonZero(binary)
        black = binary.size - white
        return white, black
    
    def compare(self, A, B):
        ''' Take two images and test for similarities '''
        pass
    
    def out_one(self, name, image):
        ''' Takes in a single window name and an image then
            displays the image to the screen. '''
        cv2.imshow(name, image)
                
    def out_multi(self, **kwargs):
        ''' Takes in window names and images and displays them to the
            screen. Use the following format:
            'Feed.out(name = image)'
            Where name is the window name and image is a numpy array '''
        for key, value in kwargs.items():
            cv2.imshow(key, value)
        
    def end_cycle(self, delay = 1):
        ''' Close all current windows and end the camera feed '''
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            self.quit()
            return True
        else:
            return False

    def quit(self):
        self.cap.release()
        cv2.destroyAllWindows()


        

class Geometry:

    def find_orientation(self, box):
        ''' Finds the global rotation of the object in relation
            to the side of the camera. 
            '''      
        center_point = self.find_center(A = box[0][0],
                                        B = box[0][2])
        adj_point = (0, center_point[1])
        
        a = self.pythag(A = box[0][0], B = box[0][1])
        b = self.pythag(A = box[0][1], B = box[0][2])
        if a > b:
            opp_point = self.find_center(A = box[0][1],
                                         B = box[0][0])
        else:
            opp_point = self.find_center(A = box[0][1],
                                         B = box[0][2])

        side1 = self.pythag(A = center_point, B = opp_point)
        side2 = self.pythag(A = opp_point,    B = adj_point)
        side3 = self.pythag(A = adj_point,    B = center_point)

        #Draw.triangle(image, (center_point, adj_point, opp_point))

        angle = self.SSS(a = side1, b = side2, c = side3)
        angle *= (180 / math.pi)
        
        if center_point[1] < opp_point[1]:
            angle = 360 - angle
        
        return center_point, angle
        
    def find_center(self, A, B):
        ''' Simple equation to find the mean point of two points '''
        y = int((A[0] + B[0]) / 2)
        x = int((A[1] + B[1]) / 2)
        return (y, x)

    def pythag(self, A, B):
        ''' Simple equation to find the distance between two points '''
        a = abs(A[0] - B[0])
        b = abs(A[1] - B[1])
        root = math.sqrt((a  **  2) + (b  **  2))
        return int(root)

    def SSS(self, a, b, c):
        ''' Simple equation to find the angle using three sides '''
        D = ((c  **  2) + (a  **  2) - (b  **  2)) / (2 * c * a)
        acosine = math.acos(D)
        return acosine


class Draw:
    
    def contours(self, contours, image):
        ''' Take contours and draw them on the given image '''
        for con in contours:
            cv2.drawContours(image, con, -1, (0, 255, 0), 2)
    
    def triangle(self, image, points):
        ''' Draws a triangle from the three points given as well
            as the points themselves for clarity '''

        lines = [(points[0], points[1]), (points[0], points[2]),
                 (points[0], points[1]), (points[1], points[2]),
                 (points[0], points[2]), (points[1], points[2])]
        
        for line in lines:
            self.draw_line(image, line[0])

        for point in points:
            self.draw_circle(image, point)

    def line(self, image, points):
        ''' Draws a line on image from the first point to the
            second point with a thickness of 2 '''
        cv2.line(image, points[0], points[1], (255, 255, 0), 2)
        
    def circle(self, image, center):
        ''' Draws a circle on image from the center
            with a radius of 2 '''
        cv2.circle(image, center, 2, (0, 0, 255), 2)

    def text(self, image, text, position):
        ''' Draws the specified text onto the image at the
            specified position '''
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, text, position, font, 0.5, (255, 0, 0), 1)


##      Find Orientation
##    
##            This is done using the
##            SSS Traingle equation to calculate angles
##            This requires each side of the traingle to be
##            known prior so three key points need to be found.
##
##            Firstly, the center point is located using the mean
##            of two opposite points
##            
##            Second, the adjacent point is located (the point
##            next to the hypotenuse) by taking the x from the
##            center point and setting the y to 0 (the side of the
##            screen)
##            
##            Finally, the last point is the center of the shortest
##            edge of the box, closest to the top of the screen. This
##            can be easily calculated by finding the difference
##            between two points (like with the center). This is done
##            only after the shortest side has been found.
##            The shortest side can be found using Pythagoras Theorum.
##            The x and y distance is calculated then using
##            a**2 + b**2 = c**2 we can find c (the side)
##
##            After comparing this to the second set of points we
##            know the shortest side and can find the final point.
##
##            Once each point is found, a final series of Pythag
##            calculations are done to find the length of the
##            newly created triangle. These are used to work out
##            the angle of rotation in relation to the screen
##
##            This angle is in radians so it's converted using
##            T * (180 / pi). There is a final comparison which checks
##            if the angle is supposed to be acute or obtuse in which 
##            case it adjusts the angle accordingly
