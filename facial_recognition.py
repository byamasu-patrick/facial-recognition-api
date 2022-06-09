import os
import PIL
import numpy as np
from numpy import genfromtxt
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import model_from_json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, ZeroPadding2D, Activation, Input, concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import MaxPooling2D, AveragePooling2D
from tensorflow.keras.layers import Concatenate
from tensorflow.keras.layers import Lambda, Flatten, Dense
from tensorflow.keras.initializers import glorot_uniform
from tensorflow.keras.layers import Layer
from tensorflow.keras import backend as K
K.set_image_data_format('channels_last')

def load_model():
    json_file = open('keras-facenet-h5/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights('keras-facenet-h5/model.h5')
    FRmodel = model
    return FRmodel

#tf.keras.backend.set_image_data_format('channels_last')
def img_to_encoding(image_path, model):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(160, 160))
    img = np.around(np.array(img) / 255.0, decimals=12)
    x_train = np.expand_dims(img, axis=0)
    embedding = model.predict_on_batch(x_train)
    return embedding / np.linalg.norm(embedding, ord=2)
def write_labels(new_user_info):
    label = open("labels/database.txt", "a")  # append mode
    label.write(new_user_info)    
    label.write("\n")
    label.close()
    
    pass
def load_labels():
    lines = -1
    with open("labels/database.txt" , 'r') as f:
        lines = f.readlines() # readlines creates a list of the lines
    print(lines)
    return lines

def load_database(model): 
    database = {}  
    data = load_labels()
    if len(data) >= 1:
        for user in data:
            user_arr = user.split(",")
            database[(user_arr[0] +" "+ user_arr[1])] = img_to_encoding("images/"+ (user_arr[0] +"_"+ user_arr[1]) +"."+ user_arr[3].replace('\n', ''), model)
        
    return database

# UNQ_C3(UNIQUE CELL IDENTIFIER, DO NOT EDIT)

def who_is_it(image_path, database, model):   

    encoding =  img_to_encoding(image_path, model)
    min_dist = 100
    
    for (name, db_enc) in database.items():
        dist = np.linalg.norm(encoding - db_enc)
        # print("Distance: "+ dist)
        # If this distance is less than the min_dist, then set min_dist to dist, and identity to name. (≈ 3 lines)
        if dist < min_dist:
            min_dist = dist
            identity = name
                
    if min_dist > 0.7:
        print("Not in the database.")
    else:
        print ("it's " + str(identity) + ", the distance is " + str(min_dist))
    return min_dist
