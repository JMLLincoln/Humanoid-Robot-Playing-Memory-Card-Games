# Humanoid-Robot-Playing-Memory-Card-Games

Again, this Readme file is a notepad for me; expect a small increase in time lost today.

---

## Goal
The goal of this project is to create the backend for a humanoid robot. It should be able to 'see' the game board, detect individual cards, select a card based on a neural network, and act accordingly (hand gestures, speech, facial expressions).
Maybe not all of the humanoid features will be implemented but I'll give it a go.

---

## Present
Currently, the modules are split apart quite a bit and should work alright one their own.
1. camera.py
	+ Has a lot of functions for processing images
	+ Can detect face up cards
	+ Can detect face down cards separately

2. game.py
	+ Prepare yourself for a text-based adventure
	+ lol jk, but you can play the 'card' game in the python shell
  
3. host.py
	+ creates a web server at localhost:8888
	+ the test website in web-files works with this one and opens a websocket using JavaScript to create a client
	+ The two can communicate but it's minimal 

4. merged.py
	+ merges game.py and host.py
	+ incredible file names, I know
	+ you can play the game in the python shell while the gui on the website is updated
	+ open index.html in web-files 
	+ then run merged.py
	+ then click 'play' on the website
	+ should work, if it doesn't then hard lines
  
5. main.py
	+ makes camera.py work 
