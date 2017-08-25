import os
import camera
import models
import numpy as np

from config import CONFIG, MODEL_NAME

_test_dir = CONFIG['testing directory']

_pre_img_size = CONFIG['pre image size']
_post_img_size = CONFIG['post image size']

_lr = CONFIG['learning rate']
_output = CONFIG['output']

_network_name = CONFIG['network name']


cam = camera.Feed()
draw = camera.Draw()

model = models.initialise(model_name = MODEL_NAME,
                          network_name = _network_name,
                          image_size = _post_img_size,
                          learning_rate = _lr,
                          output = _output)


def predict_and_parse(image_a, image_b):

    image_a = cam.resize(image_a, (200, 200))
    image_b = cam.resize(image_b, (200, 200))

    images = np.concatenate((image_a, image_b), axis = 1)
    cam.out_one('ims1', images)

    test_img = cam.resize(images, _post_img_size)
    cam.out_one('ims2', test_img)
    
    test_img = np.array([test_img]).reshape(-1, _post_img_size[0],
                                            _post_img_size[1], 1)

    results = model.predict(test_img)[0]
    
    if results[0] > results [1]:
        out_a = "Images aren't the same!"
    else:
        out_a = "It's a match!"

    out_b = "Non-Match: %s%%" % int(results[0] * 100)
    out_c = "    Match: %s%%" % int(results[1] * 100)

    return out_a, out_b, out_c


def draw_text(img, txt, pos, sze, col):

    draw.text(image = img, text = txt, position = pos,
              size = sze, colour = (50, 50, 50), thickness = 5)
        
    draw.text(image = img, text = txt, position = pos,
              size = sze, colour = col, thickness = 2)



last_message = ""
more_than = "More than two cards found..."
less_than = "Less than two cards found..."
two_found = "Two cards found. Making prediction..."

while(True):
    # Get the BGR frame of the video feed
    colour = cam.store_frame()
    # Convert the BGR image to grayscale
    gray = cam.to_gray(colour = colour)
    # Convert the grayscale image to binary
    binary = cam.to_binary(gray = gray, thresh = 150, max = 255) #185

    # Morphologically process the binary image
    #binary = cam.close((5, 5), binary)

    # Get the contours from the binary image
    contours, hierarchy = cam.get_contours(binary = binary)
    # Remove the contours which have an area outside the limits
    contours = cam.remove_contours(contours = contours,
                                   lower = 27000, upper = 35000) # 10k:25k
    
    # Create box points for each contour, outlining the cards
    cards = []
    boxes = []
    for con in contours:

        # Gets box points to be drawn later
        box = cam.create_rect(contour = con)
        boxes.append(box)

        # Uses box points to quickly find the bounding
        # rectangle of the card
        y1, x1 = np.amin(box[0], axis = 0)
        y2, x2 = np.amax(box[0], axis = 0)

        # Crops the card from the full grayscale image
        img = gray[x1:x2, y1:y2]

        # Gets information about the rotated rectangle
        # for the card; incase it is rotated
        center, size, angle = cam.get_rect(con)

        # Assigns the card a (hopefully) unique name
        # based on it's center position
        name = "(%s,%s): " % (int(center[0] / 50) * 50, int(center[1] / 50) * 50)

        # Outputs the non-rotated card as an image
        cam.out_one(name + '1', img)

        # Acquires the width and height of the bounding
        # rectangle 
        width = int(x2-x1)
        height = int(y2-y1)

        # Applies a rotation on the card, keeping the bounding
        # rectangle size to make sure there is no clipping
        # This rotation should make it upright
        img = cam.rotate_image(img, center, angle, height, width)

        # Finally, crop the upright card based on the actual
        # size of the card and the bounding rectangle
        width_diff = int(abs(width - size[0]) / 2)
        height_diff = int(abs(height - size[1]) / 2)

        # Set higher than 0 to crop the border
        border = 0
        
        new_x1 = width_diff + border
        new_x2 = width - width_diff - border
        new_y1 = height_diff + border
        new_y2 = height - height_diff - border
        
        img = img[new_x1:new_x2, new_y1:new_y2]

        # Outputs the rotated and cropped card as an image
        cam.out_one(name + '2', img)

        # Adds the card to the list to be used in the cnn
        # model later
        cards.append(img)    

    a, b, c = None, None, None
    
    if len(cards) > 2:
        this_message = more_than

    elif len(cards) < 2:
        this_message = less_than

    else:
        try:
            a, b, c = predict_and_parse(cards[0], cards[1])
            
            string = "%s\n%s\n%s" % (a, b, c)
            this_message = string
            
        except Exception as error:
            this_message = str(error)

    if not last_message == this_message:
        print("\n%s" % this_message)
        last_message = this_message

    draw.contours(contours = boxes, image = colour)
    
    if not a == None:
        draw_text(colour, a, (20, 30), 0.8, (60, 169, 224))
        draw_text(colour, b, (20, 60), 0.7, (79, 79, 214))
        draw_text(colour, c, (38, 90), 0.7, (81, 204, 87))
    
    cam.out_multi(Colour = colour, Binary = binary)

    # Safely complete a single loop and end it if necessary
    if cam.end_cycle(delay = 500):
        break
