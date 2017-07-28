# Humanoid-Robot-Playing-Memory-Card-Games

This Readme file is just a notepad for me; expect a small increase in time lost today if you want to read it.

---

## Goal
The goal of this project is to create the backend for a humanoid robot. It should be able to 'see' the game board, detect individual cards, select a card based on a neural network, and act accordingly (hand gestures, speech, facial expressions).
Maybe not all of the humanoid features will be implemented but I'll give it a go.

---

## Present
Currently, the modules are split apart quite a bit and should work alright one their own.
1. camera.py
	+ has a lot of functions for processing images
	+ can detect face up cards
	+ can detect face down cards separately
	
2. camera-main.py
	+ makes camera.py work
	
3. camera-convnet.py
	+ uses the camera module to collected images of cards and feed them into the convolutional neural network
	+ displays the the card the network thinks it is 
	+ displays the percentage of how confident it is

4. camera-with-sockets.py
	+ uses the camera module to detect cards and store information for them in a json file
	+ needs camera-main.py running 
	+ uses the json file in 'camera-with-sockets-web-files/index.html' to output to the screen

5. console.py
	+ prepare yourself for a thrilling text-based role-playing adventure
	+ lol jk, but you can play the 'card' game in the python shell

6. console-with-data-json.py
	+  similar to above but initliases the board based on the images detected through camera-main.py

7. console-with-sockets.py
	+ merges console.py and websocket-test.py
	+ incredible file names, I know
	+ you can play the game in the python shell while the gui on the website is updated
	+ open index.html in web-files 
	+ then run merged.py
	+ then click 'play' on the website
	+ should work, if it doesn't then hard lines
	
8. console-with-sockets-and-data-json.py
	+ similar to above but initliases the board based on the images detected through camera-main.py
	
9. websocket-test.py
	+ creates a web server at localhost:8888
	+ the test website in web-files works with this one and opens a websocket using JavaScript to create a client
	+ the two can communicate but it's minimal
	
10. tensorflow/convnet.py
	+ creates the training and testing datasets 
	+ based on images found in the 'tensorflow/test-image' and 'tensorflow/train-images'
	+ stores them in .npy files
	+ creates the conv net model
	+ fits the training set to the model
	+ can be used to test individual images by passing them through the neural net once trained
