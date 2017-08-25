import os
import cv2
import numpy as np

from shutil import rmtree
from config import CONFIG

_obj_dir = CONFIG['object directory']
_card_dir = CONFIG['card directory']

_card_image_size = CONFIG['card image size']
_card_border_size = CONFIG['card border size']
_card_border_colour = CONFIG['card border colour']
_card_back_colour = CONFIG['card back colour']

def load_image(object_name):

    path = "%s/%s" % (_obj_dir, object_name)

    image = cv2.imread(path, -1)

    # Option 1: Crop image to desired card size
    # This removes part of the image but keeps original look
    #image = crop_image(image)

    # Option 2: Resize image to desired card size
    # This causes squashing or stretching of the image
    image = cv2.resize(image, _card_image_size)

    image = add_border(image)

    return image

def crop_image(image):

    height, width, channels = image.shape

    cv2.imshow('unedited', image)

    if width < _card_image_size[0]:
        image = cv2.resize(image, (_card_image_size[0], height))
        width = _card_image_size[0]
        
    elif width > _card_image_size[0]:
        difference = width - _card_image_size[0]
        lower_bound = int(difference / 2)
        upper_bound = width - int(difference / 2)
        image = image[0:height, lower_bound:upper_bound]

        width = _card_image_size[0]

    cv2.imshow('width', image)
        
    if height < _card_image_size[1]:
        image = cv2.resize(image, (width, _card_image_size[1]))
        height = _card_image_size[1]

    elif height > _card_image_size[1]:
        difference = height - _card_image_size[1]
        lower_bound = int(difference / 2)
        upper_bound = height - int(difference / 2)
        image = image[lower_bound:upper_bound, 0:width]

        height = _card_image_size[1]
        
    cv2.imshow('height', image)

    return image

def add_border(image):

    top = _card_border_size[0]
    bot = _card_border_size[1]
    lef = _card_border_size[2]
    rig = _card_border_size[3]
    col = _card_border_colour

    # Actual border 
    image = cv2.copyMakeBorder(image, top, bot, lef, rig,
                               cv2.BORDER_CONSTANT,
                               value = col)
    # Black bounding box
    image = cv2.copyMakeBorder(image, 2, 2, 2, 2,
                               cv2.BORDER_CONSTANT,
                               value = (0, 0, 0))
    
    return image

def create_cards():

    print("Creating new directory...")
    os.makedirs(_card_dir)

    # Create blank card for the back
    path = "%s/%s" % (_card_dir, '_card-back.jpg')
    card_back = np.zeros((_card_image_size[1],  _card_image_size[0], 3), np.uint8)
    card_back[:,:,] = _card_back_colour
    card_back = add_border(card_back)
    cv2.imwrite(path, card_back)

    print("Populating directory with card images...")
    object_names = os.listdir(_obj_dir)

    # Create a card for each image in object directory
    for name in object_names:
        card = load_image(name)
        path = "%s/%s" % (_card_dir, name)
        
        cv2.imwrite(path, card)    

    print("Completed. Cards can be found at '%s'" % _card_dir)



if os.path.isdir(_obj_dir):

    if os.path.isdir(_card_dir):
        
        print("Card directory found at '%s'.\nContinuing will overwrite previous data. Continue?" % _card_dir)

        inp = input("(y/n): ")

        if inp == 'y':
            print("Removing previous directory...")
            rmtree(_card_dir)
            create_cards()
            
        elif inp =='n':
            print("Shutting down...")
            
        else:
            print("Incorrect input, shutting down...")

    else:
        create_cards()
        

else:
    print("Object directory not found. Make sure 'object directory' in config.py points to the folder with all the objects you want to convert to cards!")
    
