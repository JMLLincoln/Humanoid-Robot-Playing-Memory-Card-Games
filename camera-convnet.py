import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

_img_size = 50
_lr = 1e-3

path_to_dir = 'F:/Documents/GitHub/CS-2017-Project/tensorflow/'
_model_name = 'models/playingcards-%s-%s.model' % (_lr, '5conv-basic')

import tensorflow as tf

tf.reset_default_graph()

convnet = input_data(shape = [None, _img_size, _img_size, 1], name = 'input')

convnet = conv_2d(convnet, 32, 2, activation = 'relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 64, 2, activation = 'relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 32, 2, activation = 'relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 64, 2, activation = 'relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 32, 2, activation = 'relu')
convnet = max_pool_2d(convnet, 2)

convnet = fully_connected(convnet, 1024, activation = 'relu')
convnet = dropout(convnet, 0.8)

convnet = fully_connected(convnet, 3, activation = 'softmax')
convnet = regression(convnet, optimizer = 'adam', learning_rate = _lr,
                     loss = 'categorical_crossentropy')

model = tflearn.DNN(convnet, tensorboard_dir = 'log')

model.load(path_to_dir + _model_name)


import camera
import numpy as np

cam = camera.Feed()
draw = camera.Draw()

while(True):
    # Get the BGR frame of the video feed
    colour = cam.store_frame()
    # Convert the BGR image to grayscale
    gray = cam.to_gray(colour = colour)
    # Convert the grayscale image to binary
    binary = cam.to_binary(gray = gray, thresh = 140, max = 255) #185

    # Morphologically process the binary image
    #binary = cam.close((5, 5), binary)

    # Get the contours from the binary image
    contours, hierarchy = cam.get_contours(binary = binary)
    # Remove the contours which have an area outside the limits
    contours = cam.remove_contours(contours = contours,
                                   lower = 5000, upper = 35000) # 10k:25k
    
    # Create box points for each contour, outlining the cards
    boxes = []
    for con in contours:
        boxes.append(cam.create_rect(contour = con))

    for box in boxes:
        y1, x1 = np.amin(box[0], axis = 0)
        y2, x2 = np.amax(box[0], axis = 0)
        
        img = binary[x1:x2, y1:y2]

        try:
            img = cam.resize(image = img, size = (_img_size, _img_size))
        except:
            continue
     
        data = np.array(img).reshape(-1, _img_size, _img_size, 1)
        results = model.predict(data)[0]

        highestPercent = 0
        highestIndex = -1
        for i in range(len(results)):
            percent = round(results[i] * 100, 2)
            if percent > highestPercent:
                highestPercent = percent
                highestIndex = i

        num_string = "N: %s" % str(highestIndex + 1)
        per_string = str(highestPercent)[:-2] + '%'
        string = "%s, %s" % (num_string, per_string)
        
        draw.text(image = colour, text = string, position = (y1,x1-10),
                  size = 0.8, colour = (255, 255, 0), thickness = 2)

    draw.contours(contours = boxes, image = colour)
    cam.out_multi(Colour = colour, Binary = binary)

    # Safely complete a single loop and end it if necessary
    if cam.end_cycle(delay = 500):
        break
