import camera
import numpy as np
cam = camera.Feed()
geo = camera.Geometry()

while(True):
    # Get the BGR frame of the video feed
    colour = cam.store_frame()
    # Convert the BGR image to grayscale
    gray = cam.to_gray(colour)
    # Convert the grayscale image to binary
    binary = cam.to_binary(gray, 100, 255)

    # Morphologically process the binary image
    #binary = cam.close((5, 5), binary)

    # Get the contours from the binary image
    contours, hierarchy = cam.get_contours(binary)
    # Remove the contours which have an area outside the limits
    contours = cam.remove_contours(contours, 10000, 25000)
    
    # Create box points for each contour, outlining the cards
    boxes = []
    for con in contours:
        boxes.append(cam.create_rect(con))
    # Draw the box points to the colour image
    colour = cam.draw_contours(boxes, colour)

    # Create separate card images for further processing
    cards = []
    for box in boxes:
        # Find the rotation of the box in relation to the screen
        center, theta = geo.find_orientation(box)
        y1, x1 = np.amin(box[0], axis=0)
        y2, x2 = np.amax(box[0], axis=0)
        
        h, w = y2 - y1, x2 - x1
        temp = colour[x1:x2, y1:y2]
        try:
            cards.append(cam.rotate_image(temp, center, theta, h, w))
        except Exception as e:
            print(e)
            print("The game board is most likely corrupt.\n")

    # Output the colour, grayscale, and binary images
    cam.out(Colour = colour, Grayscale = gray, Binary = binary)

    try:
        # Try to output separated cards, could fail due obstacles
        cam.out(Card0 = cards[0], Card1 = cards[1], Card2 = cards[2],
                Card3 = cards[3], Card4 = cards[4])
    except:
        pass

    # Safely complete a single loop
    if cam.end_cycle():
        break
