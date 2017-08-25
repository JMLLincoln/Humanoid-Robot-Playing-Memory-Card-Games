import os
import cv2
import models
import random
import numpy as np

from config import CONFIG, MODEL_NAME

_train_dir = CONFIG['training directory']

_post_img_size = CONFIG['post image size']

_lr = CONFIG['learning rate']
_epochs = CONFIG['epochs']
_output = CONFIG['output']

_network_name = CONFIG['network name']


np_path = 'training_data.npy'

if os.path.isfile(np_path):
    print("Training set file found. Loading the data...")
    train_set = np.load(np_path)
else:
    print("Training set not found. Run create_training_data.py instead.")
    quit()

if not os.path.exists('%s.meta' % MODEL_NAME):

    print("Creating model...")
    model = models.create_model(_network_name,
                                _post_img_size[0],
                                _post_img_size[1],
                                _lr, _output)
    
    
    n = int(len(train_set) / 10)
    print("Splitting training set by %s items" % n)
    train = train_set[n:]
    test = train_set[:n]

    print("Training model...")

    X = np.array([i[0] for i in train]).reshape(-1, _post_img_size[0],
                                                _post_img_size[1], 1)
    Y = [i[1] for i in train]

    test_x = np.array([i[0] for i in test]).reshape(-1, _post_img_size[0],
                                                    _post_img_size[1], 1)
    test_y = [i[1] for i in test]


    print("Fitting model...")
    model.fit(X, Y, n_epoch = _epochs, validation_set = (test_x, test_y),
              snapshot_step = 500, show_metric = True, run_id = MODEL_NAME)

    print("Fit complete. Saving model...")
    model.save(MODEL_NAME)

else:
    print("Model meta exists. Use test_model.py instead.")
    
