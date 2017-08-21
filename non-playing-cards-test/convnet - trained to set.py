import os
import cv2
import numpy as np
from random import shuffle

_train_dir = 'F:/Documents/GitHub/CS-2017-Project/non-playing-cards-test/30objects'
#_test_dir = ''
_img_size = 50
_lr = 1e-4
_epochs = 5
_enlarge_set_by = 6

_model_name = 'models/%s-%s-%seps-2^%s.model' % (_lr, '6conv', _epochs, _enlarge_set_by)

def set_label(n):
    
    label = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0] # 29 possible cards

    label[n] = 1

    return label
    

def create_train_data():

    training_data = []

    n = 0
    for img in os.listdir(_train_dir):
        
        label = set_label(n)
        path = os.path.join(_train_dir, img)
        
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (_img_size, _img_size))
        
        training_data.append([np.array(img), np.array(label)])

        n += 1

    for i in range(_enlarge_set_by):
        training_data += training_data
        
    print(len(training_data))
    shuffle(training_data)
    
    np.save('train_data.npy', training_data)
    return training_data

if not os.path.isfile('train_data.npy'):
    print("Creating training data...")
    train_set = create_train_data()
else:
    print("Training set file found. Loading the data...")
    train_set = np.load('train_data.npy')



import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

import tensorflow as tf
tf.reset_default_graph()

convnet = input_data(shape = [None, _img_size, _img_size, 1], name = 'input')

convnet = conv_2d(convnet, 64, 2, activation = 'relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 128, 2, activation = 'relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 256, 2, activation = 'relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 128, 2, activation = 'relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 64, 2, activation = 'relu')
convnet = max_pool_2d(convnet, 2)

convnet = fully_connected(convnet, 1024, activation = 'relu')
convnet = dropout(convnet, 0.8)

convnet = fully_connected(convnet, 29, activation = 'softmax')
convnet = regression(convnet, optimizer = 'adam', learning_rate = _lr,
                     loss = 'categorical_crossentropy')

model = tflearn.DNN(convnet, tensorboard_dir = 'log')



if not os.path.exists('%s.meta' % _model_name):
    
    print("Creating model...")
    train = train_set[29:]
    test = train_set[:29]

    X = np.array([i[0] for i in train]).reshape(-1, _img_size, _img_size, 1)
    Y = [i[1] for i in train]

    test_x = np.array([i[0] for i in test]).reshape(-1, _img_size, _img_size, 1)
    test_y = [i[1] for i in test]


    print("Fitting model...")
    model.fit(X, Y, n_epoch = _epochs, validation_set = (test_x, test_y),
              snapshot_step = 500, show_metric = True, run_id = _model_name)

    print("Fit complete. Saving model...")
    model.save(_model_name)

else:
    
    print("Model meta exists. Loading model...")
    model.load(_model_name)

    test_arr = np.array([i[0] for i in test_set]).reshape(-1, _img_size, _img_size, 1)
    inp = test_arr
    results = model.predict(inp)[290]
    
    print ("\nPercentage Results:")
    for i in range(len(results)):
        percent = round(results[i] * 100, 2)
        num = i + 1
        print ("%s: %s" % (num, percent))
