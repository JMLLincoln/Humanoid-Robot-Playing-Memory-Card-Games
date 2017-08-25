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

2. conifg.py
	+ Any changes to the models should be changed here

3. create_training_data.py
	+ 

4. format_cards.py
	+ Takes all objects from '29objects'
	+ Formats them for printing
	+ Used to create cards for the physical game

5. models.py
	+ Contains all cnn models that can be used.
	+ Made it fairly easy to add more 

6. test_model_camera.py
	+ 

7. test_model_folder.py
	+ 

8. train_model.py
	+ 
