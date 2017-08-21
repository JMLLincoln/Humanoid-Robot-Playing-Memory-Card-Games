import os
import cv2
import random
import numpy as np
from random import shuffle

_objects_dir = 'F:/Documents/GitHub/CS-2017-Project/non-playing-cards-test/30objects'
_train_dir = 'F:/Documents/GitHub/CS-2017-Project/non-playing-cards-test/training-set'
_test_dir = 'F:/Documents/GitHub/CS-2017-Project/non-playing-cards-test/test-images'

_pre_img_size = 600
_post_img_size = 50

_truth_multiplier = 4
_false_samples = 200
_lr = 1e-4
_convs = '5CNV'
_epochs = 30

_model_name = 'models/Matching-%sLR-%s-%sxT-%sFS-%sEP-x2W.model' % (_lr, _convs, _truth_multiplier, _false_samples, _epochs)

def set_label(n):
    
    label = [0, 0]
    label[n] = 1
    return label
    

def create_train_images():

    labels = []
    objects = []

    # Stores all objects into a list
    for img in os.listdir(_objects_dir):

        labels.append(img)
        path = os.path.join(_objects_dir, img)
        
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (_pre_img_size, _pre_img_size))
        
        objects.append(img)
        
    # Concatenates each object onto itself and every other
    for i in range(len(objects)):
        for j in range(i, len(objects)):

            lab_1 = labels[i][:-4]
            lab_2 = labels[j][:-4]
            
            if i == j:
                match = 1
            else:
                match = 0
                
            new_lab = "%s_%s_%s" % (match, lab_1, lab_2)
            path = "%s/%s.jpg" % (_train_dir, new_lab)
            
            img_1 = objects[i]
            img_2 = objects[j]
            
            new_img = np.concatenate((img_1, img_2), axis = 1)
            cv2.imwrite(path, new_img)


def create_train_data():

    training_data = []
    true_matches = []
    false_matches = []

    for img in os.listdir(_train_dir):
        
        label = set_label(int(img[0]))
        path = os.path.join(_train_dir, img)
        
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (_post_img_size*2, _post_img_size))

        #cv2.imshow('im', img)

        if label[1] == 1:
            for i in range(_truth_multiplier):
                true_matches.append([np.array(img), np.array(label)])
                
        elif label[0] == 1:
            false_matches.append([np.array(img), np.array(label)])

    print("\nFound %s matching paris" % int((len(true_matches) / _truth_multiplier)))
    print("Multiplied by %s to make %s total matches.\n" % (_truth_multiplier, len(true_matches)))
    print("Found %s non-matching pairs" % len(false_matches))
    print("Sampled to %s total non-matches.\n" % _false_samples)

    training_data = random.sample(false_matches, _false_samples)
    training_data += true_matches

    print("Collected a total of %s images\n" % len(training_data))
    shuffle(training_data)
    
    #np.save('train_data.npy', training_data)
    return training_data


if not os.path.isdir(_train_dir):
    print("Folder not found, creating training images...")
    os.makedirs(_train_dir)
    create_train_images()
else:
    print("Folder found, attempting to load data instead...")

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

convnet = input_data(shape = [None, _post_img_size*2, _post_img_size, 1],
                     name = 'input')

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

convnet = fully_connected(convnet, 2, activation = 'softmax')
convnet = regression(convnet, optimizer = 'adam', learning_rate = _lr,
                     loss = 'categorical_crossentropy')

model = tflearn.DNN(convnet, tensorboard_dir = 'log')



if not os.path.exists('%s.meta' % _model_name):
    
    print("Creating model...")
    n = int(len(train_set) / 10)
    train = train_set[n:]
    test = train_set[:n]
    print("Split training set by %s items" % n)

    X = np.array([i[0] for i in train]).reshape(-1, _post_img_size*2,
                                                _post_img_size, 1)
    Y = [i[1] for i in train]

    test_x = np.array([i[0] for i in test]).reshape(-1, _post_img_size*2,
                                                    _post_img_size, 1)
    test_y = [i[1] for i in test]


    print("Fitting model...")
    model.fit(X, Y, n_epoch = _epochs, validation_set = (test_x, test_y),
              snapshot_step = 500, show_metric = True, run_id = _model_name)

    print("Fit complete. Saving model...")
    model.save(_model_name)

else:
    
    print("Model meta exists. Loading model...")
    model.load(_model_name)




def get_image_file(object_names, n=-1):

    if n == -1 or n >= len(object_names):
        n = random.randint(0, len(object_names)-1)

    path = "%s/%s" % (_test_dir, object_names[n])
    
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (_pre_img_size, _pre_img_size))
    
    return img, path

def draw_circle(img, colour):

    cv2.circle(img, (_pre_img_size, int(_pre_img_size/2)), 15, colour, 30)

def feed_images(a = -1, b = -1):
    
    object_names = os.listdir(_test_dir)

    if a == -1:
        test_img_1, test_path_1 = get_image_file(object_names)
    else:
        test_img_1, test_path_1 = get_image_file(object_names, a)

    if b == -1:
        test_img_2, test_path_2 = get_image_file(object_names)
    else:
        test_img_2, test_path_2 = get_image_file(object_names, b)
    
    images = np.concatenate((test_img_1, test_img_2), axis = 1)
    
    test_img = cv2.resize(images, (_post_img_size*2, _post_img_size))
    test_img = np.array([test_img]).reshape(-1, _post_img_size*2, _post_img_size, 1)
    
    results = model.predict(test_img)[0]

    print("Testing images:\n%s\n%s\n" % (test_path_1, test_path_2))
    if results[0] > results[1]:
        print("Images do not match!")
        draw_circle(images, (0, 0, 0))
    else:
        print("Images found to identical!")
        draw_circle(images, (255, 255, 255))

    cv2.imshow('Test Images', images)
        
    print("\nPercentage Results:")
    for i in range(len(results)):
        percent = round(results[i] * 100, 2)
        num = i + 1
        print ("%s: %s" % (num, percent))
