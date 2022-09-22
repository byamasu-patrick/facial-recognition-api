import os
from flask import Flask, request, jsonify
import traceback
import base64
import cv2
import numpy as np
from flask_cors import CORS, cross_origin
from facial_recognition import load_database, load_model, write_labels, verify

app = Flask(__name__)

CORS(app, support_credentials=True)

FRmodel = load_model()
database = load_database(FRmodel)
base_path = os.path.dirname(os.path.realpath(__file__)) 
# app.config['data']
# print(app.instance_path)
UPLOAD_PATH = os.path.join(os.path.dirname(__file__), "benefiary-reference", "database")
UPLOAD_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "benefiary-reference", "images")
MEDIA_FOLDER = os.path.join(os.path.dirname(__file__), "uploaded")
os.makedirs(os.path.join(os.path.dirname(__file__), UPLOAD_PATH), exist_ok=True)

def save(encoded_data, filename):
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
    print(img)
    return cv2.imwrite(filename, img)

@app.route('/uploaddata', methods = ["POST"])
@cross_origin(supports_credentials=True)
def savedata():
    if request.method == "POST":
        try:
            global FRmodel
            global database
            user_infos = request.get_json()
            id_profile = user_infos['id_picture']
            first_name = user_infos["first_name"]
            sir_name = user_infos["sir_name"]
            phone = user_infos["phone"]
            file_name = first_name.lower() + "_"+ sir_name.lower() +".png"
            
            user_info = first_name + ","+ sir_name +","+ phone +",png"
            
            write_labels(user_info)
            
            file_dir = os.path.join(os.path.dirname(__file__), UPLOAD_IMAGE_PATH, file_name)
            save(id_profile, file_dir)
                      
            FRmodel = load_model()
            database = load_database(FRmodel)
            
            return jsonify({'success': 'Data uploaded successfuly'})   
        except Exception:
            # return redirect(url_for('home'))
            print(traceback.print_exc())
    return ""
 
@app.route('/upload', methods = ["POST"])
@cross_origin(supports_credentials=True)
def upload():
    try:        
        person = request.get_json()
        base_64_image = person['upload_image']
        first_name = person['first_name']
        sir_name = person['sir_name']
        fullname = first_name.lower() + "_"+ sir_name.lower() +".png"
        file_dir = os.path.join(os.path.dirname(__file__), UPLOAD_PATH, fullname)
        save(base_64_image, file_dir)
        identity = fullname = first_name.lower() + " "+ sir_name.lower()
        
        dist, door_open = verify(file_dir, identity, database, FRmodel)
        if door_open and dist is not None:
            return jsonify({'success': True, 'result': "It's " + identity})                    
        else:
            return jsonify({'success': False, 'result': "It's not " + identity})                    
       
    except Exception:
        # return redirect(url_for('home'))
        print(traceback.print_exc())
    return ""

if __name__ == "__main__":    
    
    app.run(host='0.0.0.0', port=5000, debug=True)

# pip install bioinfokit