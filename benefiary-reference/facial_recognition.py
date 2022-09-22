import numpy as np
import tensorflow as tf
from tensorflow.keras.models import model_from_json
from tensorflow.keras import backend as K
K.set_image_data_format('channels_last')

# https://www.tensorflow.org/install/pip

def load_model():
    # Loading model data saved inside a json file
    json_file = open('keras-facenet-h5/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    # Convert the model from json model
    model = model_from_json(loaded_model_json)
    model.load_weights('keras-facenet-h5/model.h5')
    FRmodel = model
    return FRmodel

#tf.keras.backend.set_image_data_format('channels_last')
def img_to_encoding(image_path, model):
    # Enconding images into numpy array
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(160, 160))
    img = np.around(np.array(img) / 255.0, decimals=12)
    x_train = np.expand_dims(img, axis=0)
    embedding = model.predict_on_batch(x_train)
    return embedding / np.linalg.norm(embedding, ord=2)

def write_labels(new_user_info):
    # Writing data lebels
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
            database[(user_arr[0].lower() +" "+ user_arr[1].lower())] = img_to_encoding("images/"+ (user_arr[0].lower() +"_"+ user_arr[1].lower()) +"."+ user_arr[3].replace('\n', ''), model)
        
    return database

def triplet_loss(y_true, y_pred, alpha = 0.2):
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
    # Compute the (encoding) distance between the anchor and the positive
    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)), axis=-1)
    # Compute the (encoding) distance between the anchor and the negative
    neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)), axis=-1)
    # subtract the two previous distances and add alpha.
    basic_loss = tf.add(tf.subtract(pos_dist, neg_dist), alpha)
    # Take the maximum of basic_loss and 0.0. Sum over the training examples.
    loss = tf.reduce_sum(tf.maximum(basic_loss, 0.0))
    
    return loss
# UNQ_C3(UNIQUE CELL IDENTIFIER, DO NOT EDIT)

def verify(image_path, identity, database, model):
    # Compute the encoding for the image. Use img_to_encoding() see example above. (≈ 1 line)
    encoding = img_to_encoding(image_path, model)
    # Compute distance with identity's image (≈ 1 line)
    if identity in database:        
        dist = np.linalg.norm(encoding - database[identity])
        # Open the door if dist < 0.7, else don't open (≈ 3 lines)
        if dist < 0.7:
            print("It's " + str(identity) + ", welcome in!")
            door_open = True
        else:
            print("It's not " + str(identity) + ", please go away")
            door_open = False
        return dist, door_open
    return (None, False)

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
