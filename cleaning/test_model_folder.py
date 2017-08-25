import os
import cv2
import models
import numpy as np

from random import randint
from config import CONFIG, MODEL_NAME
from distutils.dir_util import copy_tree

_test_dir = CONFIG['testing directory']

_pre_img_size = CONFIG['pre image size']
_post_img_size = CONFIG['post image size']

_lr = CONFIG['learning rate']
_output = CONFIG['output']

_network_name = CONFIG['network name']


def get_image_file(object_names, n=-1):

    if n == -1 or n >= len(object_names):
        n = randint(0, len(object_names)-1)

    path = "%s/%s" % (_test_dir, object_names[n])

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, _pre_img_size)
    
    return img, path

def draw_circle(img, colour):

    cv2.circle(img, (_pre_img_size[0], int(_pre_img_size[1]/2)), 15, colour, 30)

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

    test_img = cv2.resize(images, _post_img_size)
    test_img = np.array([test_img]).reshape(-1, _post_img_size[0],
                                            _post_img_size[1], 1)

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



model = None
if os.path.isdir(_test_dir):
    print("Testing directory found, loading the model...")
    
    model = models.initialise(MODEL_NAME, _network_name,
                              _post_img_size, _lr, _output)

else:
    print("Testing directory not found. Would you like a folder to be created for you?")
    
    inp = input("(y/n): ")
    
    if inp == 'y':
        print("Creating new folder at '%s'" % _test_dir)
        os.makedirs(_test_dir)
        
        from_dir = CONFIG['object directory']
        print("Populating new directory with contents from '%s'" % from_dir)
        copy_tree(from_dir, _test_dir)
    
    elif inp =='n':
        print("Create a folder at '%s' and move some images over there to test the model." % _test_dir)
        
    else:
        print("Incorrect input, shutting down.")

