import camera
import numpy as np

cam = camera.Feed()
geo = camera.Geometry()
draw = camera.Draw()

errors = 0
cards = {}
positions = {}
first_run = True

while(True):
    # Get the BGR frame of the video feed
    colour = cam.store_frame()
    # Convert the BGR image to grayscale
    gray = cam.to_gray(colour = colour)
    # Convert the grayscale image to binary
    binary = cam.to_binary(gray = gray, lower = 185, upper = 255) #100:255

    # Morphologically process the binary image
    #binary = cam.close((5, 5), binary)

    # Get the contours from the binary image
    contours, hierarchy = cam.get_contours(binary = binary)
    # Remove the contours which have an area outside the limits
    contours = cam.remove_contours(contours = contours,
                                   lower = 20000, upper = 30000) # 10k:25k
    
    # Create box points for each contour, outlining the cards
    boxes = []
    for con in contours:
        boxes.append(cam.create_rect(contour = con))

    if not len(boxes) % 2 == 0 and first_run:
        print("Uneven number of playing cards detected. Has the board been set up?")
        cam.quit()
        break
   
    # Draw the box points to the colour image
    draw.contours(contours = boxes, image = colour)

    i = 0
    # Create separate card images for further processing 
    for box in boxes:
        # Find the rotation of the box in relation to the screen
        center, angle = geo.find_orientation(box = box)

        # Assign each card to a certain index dependant on the
        # position of the center
        # This allows better tracking of the cards where before,
        # the cards had indexes based on how close they were to 
        # the bottom right which wasn't accurate enough 
        if first_run:
            i += 1
            key = i
            positions[key] = center
        else:
            key = 0
            nearest = (0, 0)
            for k, v in positions.items():
                d1 = geo.pythag(A = center, B = v)
                d2 = geo.pythag(A = center, B = nearest)
                
                if d1 < d2:
                    nearest = v
                    key = k

            positions[key] = center
        
        y1, x1 = np.amin(box[0], axis = 0)
        y2, x2 = np.amax(box[0], axis = 0)
        
        h, w = y2 - y1, x2 - x1
        temp = colour[x1:x2, y1:y2]
        try:
            card = cam.rotate_image(image = temp, center = center,
                                    theta = angle, height = h, width = w)
            # Potentially crop card to remove background
            cards[key] = card
        except Exception as e:
            print(e)
            errors += 1
            print("%s): The game board is most likely corrupt.\n" % errors)

        if i == len(boxes):
            first_run = False

    # Output the colour, grayscale, and binary images
    cam.out_multi(Colour = colour, Grayscale = gray, Binary = binary)

    # Output each detected and rotated card
    for index, card in cards.items():
        # The following few commands draw a small circle on
        # cards that are flipped over
        gr = cam.to_gray(colour = card)
        bi = cam.to_binary(gray = gr, lower = 190, upper = 255)

        # Checks if the card is flipped and draws a small
        # circle in the corner of the window to indicate it
        w_pixels, b_pixels = cam.count_values(binary = bi)
        if w_pixels < b_pixels:
            draw.circle(image = card, center = (20, 20))

        # Draw the center position as text for reference
        draw.text(image = card, text = str(positions[index]),
                  position = (10, 60))

        # Remove inner boxes if any (find a better way please)
        if w_pixels > 0: 
            cam.out_one(name = str(index), image = card)
     
    # Safely complete a single loop and end it if necessary
    if cam.end_cycle():
        break
