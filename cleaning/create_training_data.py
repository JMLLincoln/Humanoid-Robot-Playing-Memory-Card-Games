import os
import cv2
import numpy as np

from config import CONFIG
from random import shuffle, sample

_obj_dir = CONFIG['object directory']
_train_dir = CONFIG['training directory']
_test_dir = CONFIG['testing directory']

_pre_img_size = CONFIG['pre image size']
_post_img_size = CONFIG['post image size']

_truth_multiplier = CONFIG['truth multiplier']
_false_samples = CONFIG['false samples']



def set_label(n):
    
    label = [0, 0]
    label[n] = 1
    return label
    
def create_train_images():

    labels = []
    objects = []

    # Stores all objects into a list
    for img in os.listdir(_obj_dir):

        labels.append(img)
        path = "%s/%s" % (_obj_dir, img)
        
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, _pre_img_size)
        
        objects.append(img)
        
    # Concatenates each object onto itself and every other object
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
            print(path)
            
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
        path = "%s/%s" % (_train_dir, img)
        
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        #print(_post_img_size)
        #print(path)
        img = cv2.resize(img, _post_img_size)

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

    training_data = sample(false_matches, _false_samples)
    training_data += true_matches

    print("Collected a total of %s images\n" % len(training_data))
    shuffle(training_data)

    np_path = 'training_data.npy'
    np.save(np_path, training_data)
    return training_data


if not os.path.isdir(_train_dir):
    print("Training directory not found, creating training images...")
    os.makedirs(_train_dir)
    create_train_images()
else:
    print("Training directory found, attempting to load data instead...")

print("Creating training data...")
create_train_data()
